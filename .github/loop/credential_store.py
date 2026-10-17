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
import queue
import re
import stat
import subprocess
import tempfile
import threading
import time

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


def worker_bundle(value):
    """Pinned Codex external-token file format; workers cannot rotate refresh.

    This internal CLI file contract must be checked again before changing the pin.
    """
    bundle(json.dumps(value))
    tokens = dict(value["tokens"], refresh_token="")
    return dict(value, auth_mode="chatgptAuthTokens", tokens=tokens)


def refresh(directory, timeout=90):
    """Force Codex's own refresh through App Server; no model prompt or API key.

    No token endpoint is reimplemented. Raw account data and diagnostics are
    discarded. A failed/ambiguous refresh must leave the secret's lease in place.
    """
    path = auth_file(directory)
    before = path.read_bytes()
    env = {k: os.environ[k] for k in ("PATH", "LANG", "SYSTEMROOT", "SSL_CERT_FILE", "SSL_CERT_DIR",
                                    "HTTPS_PROXY", "HTTP_PROXY", "NO_PROXY") if k in os.environ}
    env.update(CODEX_HOME=str(path.parent), CI="true")
    with tempfile.TemporaryDirectory(prefix="codex-renewal-") as scratch:
        env.update(HOME=scratch, XDG_CONFIG_HOME=scratch)
        with subprocess.Popen(["codex", "app-server", "--stdio", "-c", 'cli_auth_credentials_store="file"'],
                              cwd=scratch, env=env, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                              stderr=subprocess.DEVNULL, text=True) as process:
            events = queue.Queue()

            def read():
                try:
                    for line in process.stdout:
                        try:
                            events.put(json.loads(line))
                        except ValueError:
                            pass
                finally:
                    events.put(None)

            reader = threading.Thread(target=read, daemon=True)
            reader.start()
            deadline = time.monotonic() + timeout

            def call(identifier, method, params):
                process.stdin.write(json.dumps({"id": identifier, "method": method, "params": params}) + "\n")
                process.stdin.flush()
                while True:
                    remaining = deadline - time.monotonic()
                    if remaining <= 0:
                        raise RuntimeError("credential renewal timed out")
                    try:
                        event = events.get(timeout=remaining)
                    except queue.Empty as exc:
                        raise RuntimeError("credential renewal timed out") from exc
                    if event is None:
                        raise RuntimeError("credential renewal disconnected")
                    if isinstance(event, dict) and event.get("id") == identifier:
                        if "error" in event or not isinstance(event.get("result"), dict):
                            raise RuntimeError("credential renewal rejected")
                        return event["result"]

            try:
                call(1, "initialize", {"clientInfo": {"name": "credential-maintainer", "version": "1.0"},
                                       "capabilities": {"experimentalApi": True}})
                process.stdin.write('{"method":"initialized"}\n')
                process.stdin.flush()
                result = call(2, "account/read", {"refreshToken": True})
                account = result.get("account")
                if not isinstance(account, dict) or account.get("type") != "chatgpt":
                    raise RuntimeError("renewable ChatGPT account required")
            finally:
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait(timeout=5)
                reader.join(timeout=1)
    auth_file(directory)
    if path.read_bytes() == before:
        raise RuntimeError("credential renewal was not observed")


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
    parser.add_argument("command", choices=["check", "restore", "lease", "refresh", "persist", "remove"])
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
        elif args.command == "refresh":
            refresh(args.home)
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
