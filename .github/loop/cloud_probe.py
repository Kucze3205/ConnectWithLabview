"""Fixed no-tool model probes on an isolated cloud runner; publish summaries only.

Quota or missing credentials fail readiness. This does not launch loop sessions,
implement backend adapters, or claim a temporary login snapshot is renewable.
"""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import signal
import subprocess
import tempfile


def classify(provider, output, returncode):
    expected = f"{provider.upper()}_READY"
    answered = provider == "copilot" and output.strip() == expected
    for line in output.splitlines():
        try:
            event = json.loads(line)
        except ValueError:
            continue
        if not isinstance(event, dict):
            continue
        if provider == "claude" and event.get("type") == "result" and not event.get("is_error"):
            answered = event.get("result", "").strip() == expected
        if provider == "codex" and event.get("type") == "item.completed":
            item = event.get("item") or {}
            if item.get("type") == "agent_message":
                answered = item.get("text", "").strip() == expected
    if answered and returncode == 0:
        return "available"
    text = output.lower()
    # A generic HTTP 429 may be burst throttling, not exhausted subscription.
    if re.search(r"hit your .{0,40}limit|usage_limit_reached|quota.exceeded|insufficient_quota|premium requests.*exhaust", text):
        return "quota"
    if re.search(r"unauthorized|invalid.token|authentication.*(?:fail|required)|not logged in|401|403", text):
        return "auth_failure"
    return "unknown"


def probe(provider, timeout):
    secret = {"claude": "CLAUDE_CODE_OAUTH_TOKEN", "codex": "CODEX_AUTH_JSON", "copilot": "COPILOT_GITHUB_TOKEN"}[provider]
    value = os.environ.get(secret, "")
    report = {"provider": provider, "observed_at": datetime.now(timezone.utc).isoformat(),
              "status": "auth_failure", "reason": "missing_secret", "scope": "provider"}
    if not value:
        return report
    with tempfile.TemporaryDirectory(prefix="provider-probe-") as directory:
        root = Path(directory)
        # No runner GitHub credential, personal config, plugins or repository code.
        env = {k: os.environ[k] for k in ("PATH", "LANG", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTPS_PROXY", "HTTP_PROXY", "NO_PROXY") if k in os.environ}
        env.update(HOME=directory, XDG_CONFIG_HOME=str(root / "config"), CI="true")
        prompt = f"Reply with exactly {provider.upper()}_READY. Do not use any tools."
        if provider == "claude":
            env[secret] = value
            (root / "mcp.json").write_text('{"mcpServers":{}}')
            command = ["claude", "-p", prompt, "--tools", "", "--max-turns", "1",
                       "--output-format", "json", "--setting-sources", "",
                       "--strict-mcp-config", "--mcp-config", str(root / "mcp.json")]
        elif provider == "codex":
            auth = json.loads(value)
            (root / "auth.json").write_text(json.dumps(auth))
            (root / "auth.json").chmod(0o600)
            env["CODEX_HOME"] = directory
            command = ["codex", "exec", "--ignore-user-config", "--ephemeral", "--sandbox", "read-only",
                       "--skip-git-repo-check", "--json", prompt]
        else:
            env[secret] = value
            command = ["copilot", "-p", prompt, "--silent", "--no-ask-user", "--no-auto-update",
                       "--no-custom-instructions", "--disable-builtin-mcps",
                       "--available-tools", "view", "--deny-tool", "shell", "--deny-tool", "write"]
        with subprocess.Popen(command, cwd=directory, env=env, stdin=subprocess.DEVNULL,
                              stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                              text=True, start_new_session=True) as proc:
            try:
                output, _ = proc.communicate(timeout=timeout)
            except subprocess.TimeoutExpired:
                os.killpg(proc.pid, signal.SIGKILL)
                proc.communicate()
                return dict(report, status="unknown", reason="timeout")
        status = classify(provider, output, proc.returncode)
        report.update(status=status, reason="model_replied" if status == "available" else "model_unavailable")
        # Preserve a documented numeric reset when present; never publish raw output.
        reset = re.search(r'"resets?_?[aA]t"\s*:\s*(\d{10,13})', output)
        if reset:
            stamp = int(reset[1])
            report["retry_after"] = datetime.fromtimestamp(stamp / 1000 if stamp > 10**11 else stamp, timezone.utc).isoformat()
        # Provider-wide classification is conservative; adapters must refine scope.
        report["returncode"] = proc.returncode
        return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("provider", choices=["claude", "codex", "copilot"])
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--timeout", default=120, type=int)
    args = parser.parse_args()
    try:
        report = probe(args.provider, args.timeout)
    except (OSError, ValueError, subprocess.SubprocessError):
        report = {"provider": args.provider, "status": "unknown", "reason": "probe_failed"}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report))
    raise SystemExit(0 if report["status"] == "available" else 1)
