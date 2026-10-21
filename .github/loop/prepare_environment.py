"""Prepare pinned public sources and check actual resource/XML access, not semantics.

No credentials, package installation, NI activation or model calls are needed.
The parser is imported from the pinned checkout in a separate Python process.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import xml.etree.ElementTree as ET


def git(path, *args):
    return subprocess.run(
        ["git", "-C", str(path), *args], check=True, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=180,
    ).stdout.strip()


def prepare(cache):
    manifest = json.loads(Path(__file__).with_name("environment-sources.json").read_text())
    cache.mkdir(parents=True, exist_ok=True)
    (cache / "readiness.json").unlink(missing_ok=True)
    sources = []
    for source in manifest["sources"]:
        target = cache / source["name"]
        target.mkdir(exist_ok=True)
        if not (target / ".git").exists():
            if any(target.iterdir()):
                raise RuntimeError(f"Refusing nonempty cache without git metadata: {target}")
            git(target, "init", "-q")
        if git(target, "status", "--porcelain", "--untracked-files=no"):
            raise RuntimeError(f"Tracked changes in cache: {target}; use a fresh cache")
        found = subprocess.run(
            ["git", "-C", str(target), "cat-file", "-e", source["commit"] + "^{commit}"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=20,
        ).returncode == 0
        if not found:
            git(target, "fetch", "--quiet", "--depth=1", source["url"], source["commit"])
        git(target, "-c", "advice.detachedHead=false", "checkout", "--quiet", "--detach", source["commit"])
        if git(target, "rev-parse", "HEAD") != source["commit"]:
            raise RuntimeError(f"Wrong source revision: {target}")
        license_text = (target / source["license_file"]).read_text(encoding="utf-8")
        if source["license_marker"] not in license_text:
            raise RuntimeError(f"Unexpected license: {target}")
        sources.append({"name": source["name"], "commit": source["commit"], "license": source["license"]})

    fixture_info = manifest["fixture"]
    fixture = cache / fixture_info["source"] / fixture_info["path"]
    digest = hashlib.sha256(fixture.read_bytes()).hexdigest()
    if digest != fixture_info["sha256"]:
        raise RuntimeError("Fixture SHA256 mismatch")
    project = cache / "actor-framework" / manifest["project"]
    tree = ET.parse(project)
    if tree.getroot().tag != "Project":
        raise RuntimeError("Fixture is not a LabVIEW XML project")
    # Isolated Python ignores user PYTHONPATH; load just the pinned parser explicitly.
    code = (
        "import json,sys; sys.path.insert(0,sys.argv[1]); "
        "from pylavi.file import Resources; r=Resources.load(sys.argv[2]); "
        "assert r.types(), 'No resources parsed'; print(json.dumps(r.types()))"
    )
    env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
    parsed = subprocess.run(
        [sys.executable, "-I", "-B", "-c", code, str(cache / "pylavi"), str(fixture)],
        check=True, text=True, capture_output=True, timeout=60, env=env,
    )
    report = {
        "public_sources": "ready", "sources": sources, "cache": str(cache),
        "fixture": fixture_info["path"], "sha256": digest,
        "resource_types": json.loads(parsed.stdout),
        "project": manifest["project"], "project_lvversion": tree.getroot().get("LVVersion"),
        "labview_ide": "not_checked", "model_access": "not_checked",
        "semantic_reading": "not_measured",
    }
    (cache / "readiness.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache", required=True, type=Path)
    args = parser.parse_args()
    try:
        prepare(args.cache.resolve())
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError, ET.ParseError) as exc:
        print(f"Environment preparation failed: {exc}", file=sys.stderr)
        sys.exit(1)
