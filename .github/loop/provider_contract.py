"""Cloud-only real structured action and catalog check; publish metadata only."""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess

from provider_adapter import Failure, models, request
from tool_broker import ACTION_SCHEMA


def check(provider, codex_home=None):
    credential = os.environ.get({"claude": "CLAUDE_CODE_OAUTH_TOKEN", "codex": "CODEX_WORKER_AUTH_JSON",
                                 "copilot": "COPILOT_GITHUB_TOKEN"}[provider], "")
    if codex_home:
        from credential_store import auth_file, worker_bundle
        credential = json.dumps(worker_bundle(json.loads(auth_file(codex_home).read_text())))
    result = {"provider": provider, "observed_at": datetime.now(timezone.utc).isoformat()}
    try:
        if not credential:
            raise Failure({"status": "auth_failure", "scope": "provider", "reason": "missing_secret"})
        try:
            catalog = models(provider, credential)
        except Failure as error:
            if provider != 'copilot':
                raise
            catalog = {'source': 'provider_rpc', 'models': [], 'discovery_failure': error.observation}
        result["catalog"] = catalog
        model = "claude-sonnet-5-5" if provider == "claude" else next(
            (m["id"] for m in catalog["models"] if m["default"]),
            catalog["models"][0]["id"] if catalog['models'] else None)
        result["model"] = model
        prompt = ('Return a single JSON object matching this schema: ' + json.dumps(ACTION_SCHEMA) +
                  '. Set tool="Finish", status="done", text="BROKER_READY", and every other field to an empty string. '
                  'Do not use native tools. The parent process executes role tools.')
        metadata = {}
        action = request(provider, model, credential, prompt, metadata=metadata)
        result['execution_models'] = metadata.get('models', [])
        if (action["tool"], action["status"], action["text"]) != ("Finish", "done", "BROKER_READY"):
            raise Failure({"status": "unknown", "scope": "model", "reason": "unexpected_action"})
        result.update(status="available", scope="model", reason="structured_action_accepted")
    except Failure as error:
        result.update(error.observation)
    except (OSError, ValueError, KeyError, TypeError, RuntimeError, subprocess.SubprocessError):
        result.update(status="unknown", scope="provider", reason="transport_contract_failed")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("provider", choices=["claude", "codex", "copilot"])
    parser.add_argument("--codex-home")
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    report = check(args.provider, args.codex_home)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items() if k != "catalog"}))
    raise SystemExit(0 if report["status"] == "available" else 1)
