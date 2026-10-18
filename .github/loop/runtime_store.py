"""Engine-only durable state on a separate branch, with native GitHub CAS.

Provider availability and each session use separate files. Concurrent sessions
cannot overwrite an observation read before another session's update. No token,
login bundle or raw provider diagnostics belongs in these documents.
"""
import base64
import copy
import json
import os
import re
import subprocess
import time
from urllib.parse import quote


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
        result = subprocess.run(command, input=json.dumps(value) if value is not None else None,
                                env=env, capture_output=True, text=True, timeout=90)
        if result.returncode:
            found = re.search(r"HTTP (\d+)", result.stderr)
            raise APIError(int(found[1]) if found else 0)
        return json.loads(result.stdout) if result.stdout.strip() else None

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
