"""Inspect eight explicitly selected small fixtures, never modify them."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
import zlib

sys.dont_write_bytecode = True
BASE = Path(__file__).resolve().parents[1]
ENV = Path(os.environ.get('LABVIEW_ENVIRONMENT', '/resources/environment'))
SELECTION = [
    'pylavi/tests/add.vi',
    'actor-framework/Providers/MessageMakerProvider/_Message Maker/_support/Localized Strings.vi',
    'actor-framework/Providers/MessageMakerProvider/AFPP Shared/Constants.vi',
    'actor-framework/Providers/MessageRescripter/Support/Localized Strings.vi',
    'actor-framework/Providers/MessageMakerProvider/Support/Localized Strings.vi',
    'actor-framework/Core/ActorFramework/tracing/Support/Get Clone Name.vi',
    'actor-framework/Core/AFDebug/Get Registry Update Event.vi',
    'actor-framework/Core/ActorFramework/Specialty Messages/Reply Msg/Drop Message Core.vi',
]

def main():
    spec = importlib.util.spec_from_file_location('inspector', BASE / 'inspect_vi.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    labels = module.load_labels()
    classes = labels.get('SL_CLASS_TAGS', {})
    result = {'selection_criteria': 'Existing add discriminator baseline plus four smallest actor-framework VIs (by file size, lexical tie break; names used only for selection), and three small Core VIs selected for possible logic diversity. Eight original binaries total; no corpus heap dump. Names are not semantic evidence.', 'fixture_limit': 12, 'fixtures': []}
    for rel in SELECTION:
        path = ENV / rel
        item = {'path': rel, 'source': rel.split('/')[0]}
        try:
            raw = path.read_bytes()
            item.update(bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())
            resources = module.rsrc_resources(raw)
            item['resources'] = [{k: r[k] for k in ('type', 'id', 'payload_length')} for r in resources]
            parsed = module.inspect(path)
            module.annotate(parsed, labels)
            item.update(status=parsed['status'], heap_sha256=parsed['heap_sha256'], heap_bytes=parsed['heap_bytes'], entries=len(parsed['entries']))
            item['classes'] = sorted({classes.get(str(a['value']), str(a['value'])) for e in parsed['entries'] for a in e['attributes'] if a['id'] == -2})
            item['candidate_fields'] = [e for e in parsed['entries'] if any(s in e['name'].lower() for s in ('typeDesc'.lower(), 'datafill', 'value', 'const', 'termsof', 'primindex', 'primresid'))]
            if parsed['status'] != 'complete':
                item['failure'] = {k: parsed[k] for k in ('reason', 'failure_entry_offset', 'failure_cursor_offset')}
            # Preserve only the already-known small baseline for offline span checks.
            if rel == SELECTION[0]:
                r = parsed['resource']
                payload = raw[r['payload_offset']:r['payload_offset'] + r['payload_length']]
                item['baseline'] = {'resource': r, 'payload_hex': payload.hex(), 'heap_sha256': parsed['heap_sha256'], 'bdpw': []}
                for r in resources:
                    if r['type'] in ('BDPW', 'vers'):
                        data = raw[r['payload_offset']:r['payload_offset'] + r['payload_length']]
                        item['baseline']['bdpw' if r['type'] == 'BDPW' else 'vers'] = {'resource': r, 'hex': data.hex()}
        except (OSError, ValueError, KeyError, zlib.error) as exc:
            item['status'] = 'unavailable' if isinstance(exc, OSError) else 'failed'
            item['failure'] = str(exc)
        result['fixtures'].append(item)
        print(rel, item['status'], item.get('heap_bytes'), item.get('entries'), item.get('classes', []), item.get('failure', ''))
    (BASE / 'step3' / 'fixture-probe.json').write_text(json.dumps(result, indent=2) + '\n')

if __name__ == '__main__':
    main()
