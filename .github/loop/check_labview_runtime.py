"""Verify actual LabVIEW processing on a disposable cloud Docker worker.

The official NI image is used only for permitted analysis/build automation.
No credentials or repository checkout are mounted into the container.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import urllib.request


def verify_fixture(data, expected):
    if not data.startswith(b"RSRC") or hashlib.sha256(data).hexdigest() != expected:
        raise ValueError("Public fixture integrity check failed")


def check(output):
    spec = json.loads(Path(__file__).with_name("labview-runtime.json").read_text())
    if not re.fullmatch(r"nationalinstruments/labview:[a-z0-9-]+@sha256:[a-f0-9]{64}", spec["image"]):
        raise ValueError("Expected a digest-pinned official NI image")
    root = output.parent.resolve()
    root.mkdir(parents=True, exist_ok=True)
    output = root / output.name
    output.unlink(missing_ok=True)
    fixture_dir = root / "fixtures"
    fixture_dir.mkdir(exist_ok=True)
    # Avoid accidentally reusing extra inputs from a previous attempt.
    if any(fixture_dir.iterdir()):
        raise ValueError("Use a fresh runtime output directory")
    request = urllib.request.Request(spec["fixture"]["url"], headers={"User-Agent": "ConnectWithLabview-environment"})
    with urllib.request.urlopen(request, timeout=45) as response:
        data = response.read(1024 * 1024)
    verify_fixture(data, spec["fixture"]["sha256"])
    (fixture_dir / "empty_vifile.vi").write_bytes(data)
    shutil.copyfile(Path(__file__).with_name("labview_runtime.sh"), root / "run.sh")
    report = {
        "observed_at": datetime.now(timezone.utc).isoformat(),
        "status": "unverified", "image": spec["image"], "runtime_release": spec["runtime_release"],
        "fixture": spec["fixture"], "network": "none", "credentials": "none",
        "semantic_reading": "not_measured", "labview_2024_runtime": "not_verified",
        "all_versions": "not_verified",
    }
    name = "cwl-runtime-" + str(os.getpid())
    try:
        subprocess.run(["docker", "pull", spec["image"]], check=True, timeout=420)
        command = [
            "docker", "run", "--rm", "--name", name, "--network", "none",
            "--cpus", "2", "--memory", "8g", "--mount", f"type=bind,source={root},target=/probe",
            spec["image"], "bash", "/probe/run.sh", spec["labview_path"],
        ]
        result = subprocess.run(command, timeout=300)
        report["returncode"] = result.returncode
        if result.returncode == 0:
            console = (root / "console.log").read_text(encoding="utf-8", errors="replace")
            if "MassCompile operation succeeded" not in console:
                raise ValueError("Missing successful LabVIEW operation evidence")
            report["status"] = "loaded_and_compiled"
            report["installed_packages"] = (root / "installed-version.txt").read_text().splitlines()
            report["compiled_fixture_sha256"] = hashlib.sha256((fixture_dir / "empty_vifile.vi").read_bytes()).hexdigest()
        else:
            report["status"] = "failed"
        return report
    finally:
        subprocess.run(["docker", "rm", "--force", name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=20)
        output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    try:
        result = check(args.output)
        print(json.dumps(result, indent=2))
        sys.exit(0 if result["status"] == "loaded_and_compiled" else 1)
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        print(f"LabVIEW runtime check failed: {exc}", file=sys.stderr)
        sys.exit(1)
