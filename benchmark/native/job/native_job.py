#!/usr/bin/env python3
"""Proposed trusted host job; design only. Run with python3 -I -B.

No reader, custom VI, build, save, or controlled execution is invoked. Synthetic
self-tests exercise preservation and output-inventory checks, not LabVIEW.
"""
import argparse
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import stat
import subprocess
import sys
import tempfile
import uuid

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
NATIVE = HERE.parent
IMAGE = ('nationalinstruments/labview:2026q1-linux@sha256:'
         '597ba99260c0511475e27c04f13dd06f2f57e8ce7d3ee6c1ca289020b1f8c426')
LV_PATH = '/usr/local/natinst/LabVIEW-2026-64/labview'
GAP = ('Controlled I/O is blocked: readiness-case.json has no independent '
       'connector mapping, vectors, reset/stop procedure or comparison rules.')


def now():
    return datetime.now(timezone.utc).isoformat()


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1048576), b''):
            h.update(block)
    return h.hexdigest()


def write_json(path, data):
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + '\n', encoding='utf-8')


def safe_relative(value):
    p = PurePosixPath(value)
    if not value or p.is_absolute() or '..' in p.parts or str(p) != value:
        raise ValueError('Unsafe relative path: ' + repr(value))
    return p


def regular_under(root, relative):
    """Reject symlinks in every component; never follow an output symlink."""
    parts = safe_relative(relative).parts
    current = root
    for part in parts:
        current = current / part
        if current.is_symlink():
            raise ValueError('Symlink refused: ' + str(current))
    if not stat.S_ISREG(current.stat().st_mode):
        raise ValueError('Not a regular file: ' + str(current))
    return current


def inventory(root):
    result = {}
    for entry in sorted(root.rglob('*')):
        if entry.is_symlink():
            raise ValueError('Output symlink refused: ' + str(entry))
        if entry.is_dir():
            continue
        relative = entry.relative_to(root).as_posix()
        result[relative] = digest(regular_under(root, relative))
    return result


def expected_outputs(count):
    names = {'logs/close.log', 'logs/installed-version.txt'}
    for index in range(count):
        names.update({f'reports/{index:02d}.html',
                      f'logs/print-{index:02d}.log',
                      f'logs/console-{index:02d}.log'})
    return names


def validate(before, after, work_before, work_after, network, actual, expected):
    """Structural integrity only; never asserts native content or readiness."""
    if before != after:
        raise ValueError('Original source hash changed')
    if before != work_before or work_before != work_after:
        raise ValueError('Disposable input hash changed or copy differs')
    if network != 'none':
        raise ValueError('Container networking must be none')
    missing, extra = set(expected) - set(actual), set(actual) - set(expected)
    if missing or extra:
        raise ValueError(f'Output inventory mismatch: missing={sorted(missing)}, extra={sorted(extra)}')
    if any(not isinstance(h, str) or len(h) != 64 or
           any(c not in '0123456789abcdef' for c in h) for h in actual.values()):
        raise ValueError('Invalid output SHA256')


def validate_output_manifest(root, manifest_path):
    """Verify collected payload hashes, including every HTML report."""
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    actual = inventory(root)
    for name in ('record.json', 'output-sha256.json'):
        actual.pop(name, None)
    if manifest.get('algorithm') != 'sha256' or manifest.get('files') != actual:
        raise ValueError('Collected output manifest missing a payload or hash mismatch')


def git_status(root):
    result = subprocess.run(['git', '-C', str(root), 'status', '--porcelain',
                             '--untracked-files=all'], check=True,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            text=True, timeout=30)
    return result.stdout


def run_logged(command, log, timeout):
    # File capture: LabVIEW's long-lived child must never inherit a pipe.
    with log.open('wb') as stream:
        return subprocess.run(command, stdout=stream, stderr=subprocess.STDOUT,
                              timeout=timeout).returncode


def self_test():
    """Synthetic files only: no Docker, git, network or environment access."""
    with tempfile.TemporaryDirectory(prefix='native-job-self-test-') as directory:
        root = Path(directory)
        original, copy, outputs = root / 'source.vi', root / 'copy.vi', root / 'outputs'
        original.write_bytes(b'synthetic source, not a VI')
        shutil.copyfile(original, copy)
        outputs.mkdir()
        names = expected_outputs(2)
        for name in names:
            path = outputs / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text('synthetic fixture only\n', encoding='utf-8')
        before = {'pylavi/tests/synthetic.vi': digest(original)}
        working = {'pylavi/tests/synthetic.vi': digest(copy)}
        baseline = dict(before=before, after=deepcopy(before), work_before=working,
                        work_after=deepcopy(working), network='none',
                        actual=inventory(outputs), expected=names)
        validate(**baseline)
        rejected = []

        def reject(label, change):
            args = deepcopy(baseline)
            change(args)
            try:
                validate(**args)
            except ValueError:
                rejected.append(label)
            else:
                raise AssertionError('Accepted rejecting mutation: ' + label)

        manifest_path = outputs / 'output-sha256.json'
        manifest = {'algorithm': 'sha256', 'files': inventory(outputs)}
        write_json(manifest_path, manifest)
        validate_output_manifest(outputs, manifest_path)
        del manifest['files']['reports/00.html']
        write_json(manifest_path, manifest)
        try:
            validate_output_manifest(outputs, manifest_path)
        except ValueError:
            rejected.append('HTML missing from output manifest')
        else:
            raise AssertionError('Accepted HTML missing from output manifest')
        manifest_path.unlink()

        original.write_bytes(b'changed source')
        reject('changed source hash', lambda a: a.update(after={next(iter(before)): digest(original)}))
        missing = outputs / 'reports/00.html'
        missing.unlink()
        reject('missing output', lambda a: a.update(actual=inventory(outputs)))
        missing.write_text('synthetic fixture only\n', encoding='utf-8')
        (outputs / 'unexpected.vi').write_bytes(b'undeclared output')
        reject('extra output', lambda a: a.update(actual=inventory(outputs)))
        reject('network not none', lambda a: a.update(network='bridge'))
        copy.write_bytes(b'mutated disposable source')
        reject('changed working copy', lambda a: a.update(work_after={next(iter(before)): digest(copy)}))
        print(json.dumps({'scope': 'synthetic integrity checks only',
                          'accepted_baseline': True, 'rejected_mutations': rejected,
                          'native_executed': False, 'readiness_claim': False}, indent=2))


def inspect(output, operator):
    """Owner-installed, separately authorized trusted job entry point."""
    case_path = NATIVE / 'readiness-case.json'
    case = json.loads(case_path.read_text(encoding='utf-8'))
    spec = json.loads((REPO / '.github/loop/labview-runtime.json').read_text(encoding='utf-8'))
    if spec['image'] != IMAGE or spec['labview_path'] != LV_PATH:
        raise ValueError('Runtime pin differs from reviewed job')
    if case['controlled_io']['status'] != 'gap' or case['controlled_io']['vectors'] is not None:
        raise ValueError('Changed controlled-I/O design requires review, not automatic execution')
    env_value = os.environ.get('LABVIEW_ENVIRONMENT')
    if not env_value:
        raise ValueError('LABVIEW_ENVIRONMENT must name owner-provisioned public sources')
    environment = Path(env_value).resolve(strict=True)
    # This draft supports only the explicitly named saved-property inputs.
    vis = case['vis']
    if len(vis) != 2 or len({v['path'] for v in vis}) != len(vis):
        raise ValueError('Expected two unique declared readiness inputs')
    for vi in vis:
        safe_relative(vi['path'])
        if not vi['path'].startswith('pylavi/tests/') or not vi['path'].endswith('.vi'):
            raise ValueError('Input outside the reviewed readiness scope')
    output = output.absolute()
    if output.exists():
        raise ValueError('Use a new output directory')
    output.mkdir(parents=True)
    (output / 'logs').mkdir()
    record = json.loads((NATIVE / 'output-record.template.json').read_text(encoding='utf-8'))
    record.update(job_id='native-inspection-' + uuid.uuid4().hex,
                  operator_identity=operator, recipe_id=case['id'],
                  recipe_revision=case['schema_version'], recipe_sha256=digest(case_path),
                  started_at=now(), status='inspection-incomplete-not-ready',
                  outputs=[], input_identities=[], original_before_after_sha256=[],
                  working_copy_before_after_sha256=[], slot_results=[], operations_attempted=[])
    record['independent_check']['unresolved'] = [GAP,
        'Separate session must inspect substantive native values, locators and capture regions.',
        'Print operation, native property coverage, diagram content and safe loading are unverified.']
    original_before, original_after, work_before, work_after = {}, {}, {}, {}
    source_before = source_after = None
    network = 'none'
    errors = []
    container_name = 'cwl-native-' + uuid.uuid4().hex
    originals = {}
    raw_inventory = {}
    command = []
    returncode = None
    temporary = tempfile.TemporaryDirectory(prefix='cwl-native-')
    probe = Path(temporary.name)
    work = probe / 'inputs'
    raw = probe / 'outputs'
    work.mkdir()
    (raw / 'logs').mkdir(parents=True)
    (raw / 'reports').mkdir()
    try:
        source_before = git_status(environment / 'pylavi')
        if source_before:
            raise ValueError('Public source checkout must start clean')
        for vi in vis:
            relative = vi['path']
            source = regular_under(environment, relative)
            originals[relative] = source
            original_before[relative] = digest(source)
            if original_before[relative] != vi['sha256']:
                raise ValueError('Declared source SHA256 mismatch: ' + relative)
            destination = work / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, destination)
            work_before[relative] = digest(destination)
            record['input_identities'].append({'path': relative, 'sha256': vi['sha256']})
            record['operations_attempted'].append({
                'operation': 'PrintToSingleFileHtml', 'input': relative,
                'status': 'unverified-operation-and-parameters'})
        # The container receives two named VIs and this trusted script only;
        # neither the environment, repository, Docker socket nor credentials mount.
        shutil.copyfile(HERE / 'native_job.sh', probe / 'run.sh')
        pull_code = run_logged(['docker', 'pull', IMAGE], output / 'logs/docker-pull.log', 420)
        if pull_code:
            raise ValueError('Pinned image pull failed')
        command = ['docker', 'run', '--rm', '--name', container_name,
                   '--network', network, '--cpus', '2', '--memory', '8g',
                   '--mount', f'type=bind,source={probe},target=/probe',
                   IMAGE, 'bash', '/probe/run.sh', LV_PATH]
        command.extend(v['path'] for v in vis)
        returncode = run_logged(command, output / 'logs/docker-run.log', 300)
        if returncode:
            raise ValueError(f'Container operation failed: {returncode}')
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        errors.append(str(exc))
    finally:
        try:
            # Also runs after timeout; do not leave the LabVIEW process/container.
            cleanup = run_logged(['docker', 'rm', '--force', container_name],
                                 output / 'logs/docker-cleanup.log', 20)
            if cleanup not in (0, 1):
                errors.append('Unexpected Docker cleanup return code: ' + str(cleanup))
        except (OSError, subprocess.SubprocessError) as exc:
            errors.append('Container cleanup failed: ' + str(exc))
        try:
            source_after = git_status(environment / 'pylavi')
            for relative, source in originals.items():
                original_after[relative] = digest(regular_under(environment, relative))
                target = work / relative
                if target.exists():
                    work_after[relative] = digest(regular_under(work, relative))
            raw_inventory = inventory(raw)
            validate(original_before, original_after, work_before, work_after,
                     network, raw_inventory, expected_outputs(len(vis)))
            if len(original_before) != len(vis):
                raise ValueError('Not all declared inputs were staged')
            if source_before != source_after or source_after:
                raise ValueError('Source git status is not clean and unchanged')
            if any((raw / p).stat().st_size == 0 for p in raw_inventory):
                raise ValueError('Empty native output; content remains unverified')
        except (OSError, ValueError, subprocess.SubprocessError) as exc:
            errors.append('Preservation/output validation: ' + str(exc))
        # Copy only regular allowlisted outputs. Unexpected artifacts are not
        # published; their existence is an explicit failure in job.log.
        for relative in sorted(set(raw_inventory) & expected_outputs(len(vis))):
            try:
                source = regular_under(raw, relative)
                destination = output / relative
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source, destination)
            except (OSError, ValueError) as exc:
                errors.append('Output collection: ' + str(exc))
        record['actual_environment'] = {
            'image': IMAGE, 'runtime_release': spec['runtime_release'],
            'labview_path': LV_PATH, 'network': network, 'credentials': 'none',
            'docker_command': command, 'returncode': returncode,
            'native_version_build_bitness_modules_licence': 'unverified; inspect logs separately',
            'host_model_family': 'OpenAI GPT-6.1 (Codex, gpt-6.1-sol)'}
        record['source_git_status_before_after'] = {
            'command': 'git status --porcelain --untracked-files=all',
            'root': 'LABVIEW_ENVIRONMENT/pylavi', 'before': source_before, 'after': source_after}
        for relative in sorted(original_before):
            record['original_before_after_sha256'].append({
                'path': relative, 'before': original_before[relative],
                'after': original_after.get(relative)})
            record['working_copy_before_after_sha256'].append({
                'path': relative, 'before': work_before.get(relative),
                'after': work_after.get(relative)})
        for index, vi in enumerate(vis):
            for expected in vi['expected_properties']:
                record['slot_results'].append({
                    'slot_id': vi['path'] + ':' + expected['property'],
                    'reader_observation_id': None, 'native_locator': None,
                    'value': None, 'status': 'unavailable', 'evidence': [],
                    'reason': 'HTML printing does not establish this typed native property; mapping unverified.',
                    'uncertainty': 'Requires independently reviewed native API and original-object mapping.'})
        record['status'] = ('failed-not-ready' if errors else 'inspection-collected-unverified-not-ready')
        record['ended_at'] = now()
        log = {'scope': 'inspection draft; no readiness or quality verdict',
               'controlled_io_gap': GAP, 'errors': errors,
               'observed_container_output_inventory': raw_inventory,
               'separate_comparison': 'pending; no substantive native agreement asserted'}
        write_json(output / 'logs/job.log', log)
        # Avoid self-referential hashes: manifest covers collected reports/logs;
        # record lists them plus the manifest, and does not hash itself.
        payloads = inventory(output)
        write_json(output / 'output-sha256.json', {
            'algorithm': 'sha256', 'files': payloads,
            'scope': 'Collected reports/logs only; excludes record and this manifest.'})
        validate_output_manifest(output, output / 'output-sha256.json')
        payloads['output-sha256.json'] = digest(output / 'output-sha256.json')
        record['outputs'] = [{'path': p, 'sha256': h, 'status': 'produced-unverified'}
                             for p, h in sorted(payloads.items())]
        write_json(output / 'record.json', record)
        temporary.cleanup()
    print(json.dumps({'status': record['status'], 'output': str(output), 'errors': errors}))
    return 1 if errors else 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--self-test', action='store_true')
    parser.add_argument('--output', type=Path)
    parser.add_argument('--operator-identity')
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return 0
    if args.output is None or not args.operator_identity:
        parser.error('--output and --operator-identity are required for a trusted inspection job')
    try:
        return inspect(args.output, args.operator_identity)
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        print('Native inspection failed before staging: ' + str(exc), file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
