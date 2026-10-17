"""Trusted Codex credential round trip. Never run in an agent's checkout.

Environment secrets are read after the provider job lock. Replace the stored
bundle with a non-secret lease before starting Codex. Interrupted refresh or a
failed write-back then requires reseeding rather than reusing an obsolete token.
The store writer's GitHub App token belongs only to lease/persist subprocesses.
"""
import argparse
import json
import os
from pathlib import Path
import re
import stat
import subprocess

ENVIRONMENT = "provider-codex"
SECRET = "CODEX_CI_AUTH_JSON"


def bundle(text):
    value = json.loads(text)
    if not isinstance(value, dict) or value.get("auth_mode") != "chatgpt" or value.get("OPENAI_API_KEY"):
        raise ValueError("managed ChatGPT credential required")
    tokens = value.get("tokens")
    if not isinstance(tokens, dict) or any(not isinstance(tokens.get(k), str) or not tokens[k]
                                          for k in ("id_token", "access_token", "refresh_token")):
        raise ValueError("complete renewable token bundle required")
    return value


def home_path(directory, create=False):
    home = Path(directory)
    if not home.is_absolute() or home.is_symlink():
        raise ValueError("absolute private credential directory required")
    if create:
        home.mkdir(mode=0o700, parents=True, exist_ok=True)
    if not home.is_dir() or home.resolve() != home:
        raise ValueError("credential directory must not redirect")
    if os.name != "nt" and stat.S_IMODE(home.stat().st_mode) & 0o077:
        raise ValueError("credential directory must be private")
    # Do not put credentials in a checkout or artifact directory.
    for root in (Path.cwd(), Path(os.environ.get("GITHUB_WORKSPACE", Path.cwd()))):
        if home == root.resolve() or root.resolve() in home.parents:
            raise ValueError("credential directory must be outside the workspace")
    return home


def auth_file(directory):
    path = home_path(directory) / "auth.json"
    info = path.lstat()
    if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
        raise ValueError("credential must be a regular unlinked file")
    if os.name != "nt" and stat.S_IMODE(info.st_mode) & 0o077:
        raise ValueError("credential file must be private")
    bundle(path.read_text(encoding="utf-8"))
    return path


def restore(directory, text):
    value = bundle(text)
    home = home_path(directory, create=True)
    descriptor = os.open(home / "auth.json", os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(descriptor, "w", encoding="utf-8") as fh:
        json.dump(value, fh)
    return auth_file(directory)


def write_secret(text, repository, token, run=subprocess.run):
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repository or "") or not token:
        raise ValueError("repository and scoped secret-store token required")
    env = {k: os.environ[k] for k in ("PATH", "HOME", "SYSTEMROOT", "SSL_CERT_FILE", "SSL_CERT_DIR") if k in os.environ}
    env.update(GH_TOKEN=token, GH_PROMPT_DISABLED="1")
    # No credential in argv, shell interpolation, stdout, logs or Actions outputs.
    result = run(["gh", "secret", "set", SECRET, "--env", ENVIRONMENT, "--repo", repository],
                 input=text, env=env, text=True, capture_output=True, check=False, timeout=60)
    if result.returncode:
        raise RuntimeError("secret-store write failed")


def lease(directory, repository, token, run_id, writer=write_secret):
    auth_file(directory)  # reject stale lease or invalid seed before changing the store
    if not re.fullmatch(r"[0-9]+", run_id or ""):
        raise ValueError("Actions run identity required")
    writer(json.dumps({"state": "leased", "run_id": run_id}), repository, token)


def persist(directory, repository, token, writer=write_secret):
    path = auth_file(directory)
    text = path.read_text(encoding="utf-8")
    bundle(text)
    writer(text, repository, token)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["check", "restore", "lease", "persist", "remove"])
    parser.add_argument("--home", required=True)
    args = parser.parse_args()
    try:
        if args.command == "check":
            auth_file(args.home)
        elif args.command == "restore":
            restore(args.home, os.environ.get("CODEX_AUTH_JSON", ""))
        elif args.command == "lease":
            lease(args.home, os.environ.get("GITHUB_REPOSITORY"), os.environ.get("CREDENTIAL_STORE_TOKEN"),
                  os.environ.get("GITHUB_RUN_ID"))
        elif args.command == "persist":
            persist(args.home, os.environ.get("GITHUB_REPOSITORY"), os.environ.get("CREDENTIAL_STORE_TOKEN"))
        else:
            home = home_path(args.home)
            # Never recurse over a computed path or follow a credential symlink.
            path = home / "auth.json"
            if path.is_symlink():
                raise ValueError("credential file redirected")
            path.unlink(missing_ok=True)
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError):
        print(json.dumps({"operation": args.command, "status": "failed", "reason": "credential_store_not_ready"}))
        return 1
    print(json.dumps({"operation": args.command, "status": "ok"}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
