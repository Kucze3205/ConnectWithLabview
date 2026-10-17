"""A model probe sees its scratch home, system runtimes and its own processes.

Keep the credential maintainer, Actions files and other credentials outside this
mount/PID namespace. Network remains available for the provider connection.
This is a no-workspace probe boundary, not the eventual task-tool sandbox.
"""
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def sandbox(command, directory):
    root = Path(directory).resolve()
    if sys.platform != "linux" or not shutil.which("bwrap") or not root.is_dir():
        raise OSError("cloud probe isolation unavailable")
    args = ["bwrap", "--unshare-pid", "--unshare-ipc", "--unshare-uts", "--new-session", "--die-with-parent"]
    for system in ("/usr", "/bin", "/sbin", "/lib", "/lib64", "/etc", "/opt", "/run/systemd/resolve"):
        if os.path.exists(system):
            args += ["--ro-bind", system, system]
    return args + ["--dev", "/dev", "--proc", "/proc", "--tmpfs", "/tmp",
                   "--bind", str(root), str(root), "--chdir", str(root), "--"] + command


def check():
    with tempfile.TemporaryDirectory(prefix="probe-boundary-") as directory:
        outside = Path(directory, "credential-sentinel")
        outside.write_text("synthetic-secret")
        root = Path(directory, "visible")
        root.mkdir()
        code = ("import pathlib; "
                "assert not pathlib.Path(" + repr(str(outside)) + ").exists(); "
                "assert not pathlib.Path('/proc/" + str(os.getpid()) + "/environ').exists(); "
                "pathlib.Path('proof').write_text('isolated')")
        result = subprocess.run(sandbox([sys.executable, "-c", code], root), env={"PATH": os.environ["PATH"]},
                                capture_output=True, text=True, timeout=15)
        if result.returncode or not (root / "proof").exists():
            raise RuntimeError("cloud probe isolation check failed")


if __name__ == "__main__":
    check()
    print("probe boundary: external files and parent processes unavailable")
