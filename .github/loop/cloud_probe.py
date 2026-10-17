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


def classify_result(provider, output, returncode, now=None):
    """Availability evidence, not a credential-renewal or session-adapter verdict.

    Only an exact final answer counts as success. HTTP 403 alone cannot distinguish
    a revoked credential from missing model entitlement; leave it unknown.
    """
    expected = f"{provider.upper()}_READY"
    answered = provider == "copilot" and output.strip() == expected
    events = []
    for line in output.splitlines():
        try:
            event = json.loads(line)
        except ValueError:
            continue
        if not isinstance(event, dict):
            continue
        events.append(event)
        if provider == "claude" and event.get("type") == "result" and not event.get("is_error"):
            answered = event.get("result", "").strip() == expected
        if provider == "codex" and event.get("type") == "item.completed":
            item = event.get("item") or {}
            if item.get("type") == "agent_message":
                answered = item.get("text", "").strip() == expected
    if answered and returncode == 0:
        return {"status": "available", "reason": "model_replied", "scope": "model"}
    text = output.lower()
    reason, status, scope = "unclassified_failure", "unknown", "provider"
    if re.search(r"model.{0,80}(?:not found|not available|not supported|not authorized|access denied)|"
                 r"(?:no access|not have access|not entitled|not authorized).{0,80}model|"
                 r"model_not_found|model_not_allowed|unsupported_model", text):
        status, reason, scope = "entitlement_failure", "model_access_denied", "model"
    elif re.search(r"unauthorized|invalid[ _-]?(?:access[ _-]?)?token|token.{0,30}(?:expired|revoked)|"
                   r"refresh_token_reused|authentication.{0,30}(?:fail|required)|not logged in|\b401\b", text):
        status, reason = "auth_failure", "credential_rejected"
    # A generic HTTP 429 may be burst throttling, not exhausted subscription.
    elif re.search(r"hit your .{0,40}limit|usage_limit_reached|quota.exceeded|insufficient_quota|premium requests.*exhaust", text):
        status, reason = "quota", "subscription_exhausted"
        if re.search(r"model[ _-]quota|model.{0,40}limit.{0,20}reached", text):
            scope = "model"
    elif re.search(r"\b429\b|too many requests|rate[ _-]limit", text):
        status, reason = "throttled", "request_throttled"
    elif re.search(r"econnreset|econnrefused|enotfound|etimedout|network.{0,30}(?:error|unreachable)|"
                   r"connection.{0,30}(?:failed|refused|reset)|getaddrinfo|could not resolve|dns|tls|certificate verify", text):
        status, reason = "network_failure", "transport_failed"
    elif re.search(r"\b(?:500|502|503|504|529)\b|service unavailable|overloaded", text):
        status, reason = "service_failure", "provider_unavailable"
    elif re.search(r"\b403\b|forbidden", text):
        reason = "access_denied_unspecified"
    report = {"status": status, "reason": reason, "scope": scope}
    # Preserve only an explicit, future machine-readable reset. A retry delay
    # and a subscription reset are different facts; never infer one from the other.
    observed = now or datetime.now(timezone.utc)
    resets = []

    def collect(value):
        if isinstance(value, dict):
            for key, entry in value.items():
                if key in {"resetsAt", "resetAt", "resets_at", "reset_at"} and type(entry) in (int, float):
                    try:
                        reset = datetime.fromtimestamp(entry / 1000 if entry > 10**11 else entry, timezone.utc)
                        if reset > observed:
                            resets.append(reset)
                    except (ValueError, OverflowError, OSError):
                        pass
                elif isinstance(entry, (dict, list)):
                    collect(entry)
        elif isinstance(value, list):
            for entry in value:
                collect(entry)

    for event in events:
        collect(event)
    if status == "quota" and resets:
        report["retry_after"] = max(resets).isoformat()
        report["reset_source"] = "provider_timestamp"
    return report


def classify(provider, output, returncode):
    """Compatibility for callers that need only the availability category."""
    return classify_result(provider, output, returncode)["status"]


def probe(provider, timeout, codex_home=None):
    secret = {"claude": "CLAUDE_CODE_OAUTH_TOKEN", "codex": "CODEX_AUTH_JSON", "copilot": "COPILOT_GITHUB_TOKEN"}[provider]
    value = os.environ.get(secret, "")
    if provider == "codex" and codex_home is not None:
        from credential_store import auth_file
        value = auth_file(codex_home).read_text(encoding="utf-8")
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
            if codex_home is None:
                (root / "auth.json").write_text(json.dumps(auth))
                (root / "auth.json").chmod(0o600)
            env["CODEX_HOME"] = str(codex_home) if codex_home is not None else directory
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
        report.update(classify_result(provider, output, proc.returncode))
        report["returncode"] = proc.returncode
        return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("provider", choices=["claude", "codex", "copilot"])
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--timeout", default=120, type=int)
    parser.add_argument("--codex-home", type=Path, help="trusted external credential directory, retained for write-back")
    args = parser.parse_args()
    try:
        if args.codex_home is not None and args.provider != "codex":
            raise ValueError("credential directory is only supported for Codex")
        report = probe(args.provider, args.timeout, args.codex_home)
    except (OSError, ValueError, subprocess.SubprocessError):
        report = {"provider": args.provider, "status": "unknown", "reason": "probe_failed"}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report))
    raise SystemExit(0 if report["status"] == "available" else 1)
