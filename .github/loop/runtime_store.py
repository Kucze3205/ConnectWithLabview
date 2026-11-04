"""Engine-only durable state on a separate branch, with native GitHub CAS.

Provider availability and each session use separate files. Concurrent sessions
cannot overwrite an observation read before another session's update. No token,
login bundle or raw provider diagnostics belongs in these documents.
"""
import base64
import copy
import hashlib
import json
import os
import re
import subprocess
import time
from urllib.parse import quote


RETRY_PAUSES_S = (2, 8)     # GitHub's 5xx responses pass within seconds; writes are compare-and-swap, so a repeat is safe


class APIError(RuntimeError):
    def __init__(self, status):
        super().__init__("runtime state API unavailable (HTTP %s)" % status)
        self.status = status


class GitHubBackend:
    def __init__(self, repository, branch="loop-runtime", base="main"):
        if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repository):
            raise ValueError("invalid runtime repository")
        if not re.fullmatch(r"[A-Za-z0-9_-]+", branch):
            raise ValueError("invalid runtime branch")
        self.repo, self.branch, self.base = repository, branch, base

    def api(self, method, path, value=None):
        env = {k: os.environ[k] for k in ("PATH", "HOME", "SYSTEMROOT", "SSL_CERT_FILE", "SSL_CERT_DIR") if k in os.environ}
        env.update(GH_TOKEN=os.environ.get("GH_TOKEN", ""), GH_PROMPT_DISABLED="1")
        command = ["gh", "api", "repos/" + self.repo + "/" + path, "--method", method]
        if value is not None:
            command += ["--input", "-"]
        for pause in (*RETRY_PAUSES_S, None):
            result = subprocess.run(command, input=json.dumps(value) if value is not None else None,
                                    env=env, capture_output=True, text=True, timeout=90)
            if not result.returncode:
                return json.loads(result.stdout) if result.stdout.strip() else None
            found = re.search(r"HTTP (\d+)", result.stderr)
            status = int(found[1]) if found else 0
            if pause is None or 0 < status < 500:       # a 404 or 409 is an answer; 0 means no response at all
                raise APIError(status)
            time.sleep(pause)

    def initialize(self):
        try:
            self.api("GET", "git/ref/heads/" + self.branch)
            return
        except APIError as error:
            if error.status != 404:
                raise
        base = self.api("GET", "git/ref/heads/" + quote(self.base, safe="/"))
        try:
            self.api("POST", "git/refs", {"ref": "refs/heads/" + self.branch, "sha": base["object"]["sha"]})
        except APIError as error:
            if error.status != 422:
                raise
            self.api("GET", "git/ref/heads/" + self.branch)  # another session initialized it

    def read(self, key):
        try:
            value = self.api("GET", "contents/" + key + "?ref=" + self.branch)
        except APIError as error:
            if error.status == 404:
                return {}, None
            raise
        encoded = value.get("content")
        if not encoded:
            encoded = self.api("GET", "git/blobs/" + value["sha"])["content"]
        return json.loads(base64.b64decode(encoded)), value["sha"]

    def write(self, key, value, expected):
        encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
        if len(encoded) > 16_000_000:
            raise ValueError("checkpoint exceeds the durable state file limit")
        body = {"branch": self.branch, "message": "engine checkpoint: " + key,
                "content": base64.b64encode(encoded).decode()}
        if expected:
            body["sha"] = expected
        try:
            self.api("PUT", "contents/" + key, body)
            return True
        except APIError as error:
            if error.status in {409, 422}:
                return False
            raise


class LocalBackend:
    """The session job's copy of the state (ADR-0006: no GitHub token next to the model). `stage` seeds it from
    `loop-runtime`; the epilogue validates what the session left and publishes it (`publish`)."""

    def __init__(self, directory):
        self.root = os.path.abspath(directory)

    def path(self, key):
        return os.path.join(self.root, *key.split("/"))

    def read(self, key):
        try:
            with open(self.path(key), "rb") as fh:
                raw = fh.read()
        except FileNotFoundError:
            return {}, None
        return json.loads(raw), hashlib.sha256(raw).hexdigest()

    def write(self, key, value, expected):
        if self.read(key)[1] != expected:
            return False
        os.makedirs(os.path.dirname(self.path(key)), exist_ok=True)
        with open(self.path(key), "w", encoding="utf-8") as fh:
            json.dump(value, fh, sort_keys=True, separators=(",", ":"))
        return True


def newer(remote, local):
    """Per provider/model record, the newer observation wins: concurrent sessions each publish what they saw."""
    from provider_pool import _time
    out = copy.deepcopy(remote)
    for scope in ("providers", "models"):
        for provider, value in (local.get(scope) or {}).items():
            if scope == "providers":
                pairs, target = [(provider, value)], out.setdefault(scope, {})
            else:
                pairs, target = list(value.items()), out.setdefault(scope, {}).setdefault(provider, {})
            for key, record in pairs:
                if key not in target or _time(record["observed_at"]) > _time(target[key]["observed_at"]):
                    target[key] = record
    return out


def publish(store, owner, pool, session_key, session):
    """Epilogue: write the session's runtime state back as data. An invalid pool document is dropped, never trusted."""
    import provider_pool
    if isinstance(pool, dict) and isinstance(pool.get("availability", {}), dict):
        try:
            provider_pool._state(owner, pool.get("availability", {}))
        except (ValueError, TypeError, KeyError):
            pool = None
        else:
            def change(document):
                document["availability"] = newer(document.get("availability", {}), pool.get("availability", {}))
                if isinstance(pool.get("credentials"), dict):
                    document.setdefault("credentials", {}).update(
                        {k: v for k, v in pool["credentials"].items() if k in owner["providers"] and isinstance(v, str)})
                return document
            store.update("pool.json", change)
    if isinstance(session, dict) and session:
        store.update(session_key, lambda _: session)


class Store:
    def __init__(self, backend):
        self.backend = backend

    def key(self, key):
        if not re.fullmatch(r"(?:[a-z0-9_-]+/)*[a-z0-9_-]+\.json", key):
            raise ValueError("invalid runtime state key")
        return key

    def read(self, key):
        return self.backend.read(self.key(key))[0]

    def update(self, key, change):
        key = self.key(key)
        for attempt in range(12):
            current, revision = self.backend.read(key)
            updated = change(copy.deepcopy(current))
            if not isinstance(updated, dict):
                raise ValueError("runtime state must be an object")
            if self.backend.write(key, updated, revision):
                return updated
            time.sleep(min(0.05 * (attempt + 1), 0.5))
        raise RuntimeError("runtime checkpoint contention did not settle")
