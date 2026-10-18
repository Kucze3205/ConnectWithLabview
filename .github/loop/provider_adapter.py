"""Isolated model transports. Only structured proposals cross into role tools.

Full renewable credentials and GitHub write authority never enter these CLIs.
Catalogs are observations, not automatic permission to select newly added models.
"""
from contextlib import contextmanager
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import tempfile

from cloud_probe import classify_result
from probe_isolation import sandbox
from provider_rpc import RPC
from tool_broker import ACTION_SCHEMA, validate


class Failure(RuntimeError):
    def __init__(self, observation):
        super().__init__("model request did not produce an accepted action")
        self.observation = observation


def failure(provider, value):
    # Classify in memory; never retain raw account/provider diagnostics.
    return Failure(classify_result(provider, json.dumps(value), 1))


def checked(provider, result):
    if not isinstance(result, dict) or "rpc_error" in result:
        raise failure(provider, result)
    return result


@contextmanager
def isolated(provider, credential, timeout):
    with tempfile.TemporaryDirectory(prefix="model-transport-") as directory:
        root = Path(directory)
        env = {k: os.environ[k] for k in ("PATH", "LANG", "SSL_CERT_FILE", "SSL_CERT_DIR",
                                        "HTTPS_PROXY", "HTTP_PROXY", "NO_PROXY") if k in os.environ}
        env.update(HOME=directory, XDG_CONFIG_HOME=str(root / "config"), CI="true")
        if provider == "claude":
            env["CLAUDE_CODE_OAUTH_TOKEN"] = credential
            (root / "mcp.json").write_text('{"mcpServers":{}}')
            yield root, env, None
            return
        if provider == "codex":
            # Login tokens arrive over stdin and remain in memory. Native read
            # tools cannot find an auth file or a token in the process env.
            command = ["codex", "app-server", "--stdio", "-c", 'cli_auth_credentials_store="ephemeral"',
                       "-c", "features.shell_tool=false", "-c", 'web_search="disabled"',
                       "--disable", "apps", "--disable", "plugins", "--disable", "multi_agent",
                       "--disable", "code_mode", "--disable", "view_image"]
            framing = "lines"
        elif provider == "copilot":
            env.update(COPILOT_SDK_AUTH_TOKEN=credential, COPILOT_DISABLE_KEYTAR="1")
            command = ["copilot", "--headless", "--no-auto-update", "--stdio", "--no-auto-login",
                       "--auth-token-env", "COPILOT_SDK_AUTH_TOKEN"]
            framing = "headers"
        else:
            raise ValueError("unsupported model provider")
        with RPC(sandbox(command, root), cwd=root, env=env, timeout=timeout, framing=framing) as rpc:
            if provider == "codex":
                checked(provider, rpc.call("initialize", {"clientInfo": {"name": "loop-broker", "version": "1.0"},
                                                          "capabilities": {"experimentalApi": True}}))
                rpc.send("initialized")
                auth = json.loads(credential)
                if auth.get("auth_mode") != "chatgptAuthTokens" or auth.get("tokens", {}).get("refresh_token"):
                    raise ValueError("access-only Codex credentials required")
                tokens = auth["tokens"]
                account = tokens.get("account_id")
                if not account or not tokens.get("access_token"):
                    raise ValueError("Codex account identity required")
                checked(provider, rpc.call("account/login/start", {"type": "chatgptAuthTokens",
                                                                 "accessToken": tokens["access_token"],
                                                                 "chatgptAccountId": account}))
            else:
                result = rpc.call("connect", {})
                error = result.get("rpc_error", {}) if isinstance(result, dict) else {}
                if error.get("code") == -32601 or "Unhandled method" in str(error.get("message", "")):
                    result = rpc.call("ping", {"message": "loop-broker"})
                checked(provider, result)
            yield root, env, rpc


def models(provider, credential, timeout=90):
    if provider == "claude":
        # Claude has no supported catalog RPC. These are the pinned engine's
        # configured IDs, which still require a successful real request.
        return {"source": "engine_config", "models": []}
    with isolated(provider, credential, timeout) as (_, _, rpc):
        entries, cursor = [], None
        while True:
            params = {"limit": 100, "includeHidden": False} if provider == "codex" else {}
            if cursor:
                params["cursor"] = cursor
            result = checked(provider, rpc.call("model/list" if provider == "codex" else "models.list", params))
            entries += result.get("data" if provider == "codex" else "models", [])
            following = result.get("nextCursor") if provider == "codex" else None
            if not following:
                break
            if following == cursor or len(entries) > 1000:
                raise failure(provider, {"message": "invalid model catalog pagination"})
            cursor = following
        catalog = []
        for entry in entries:
            identifier = entry.get("model", entry.get("id")) if provider == "codex" else entry.get("id")
            if isinstance(identifier, str) and identifier:
                catalog.append({"id": identifier, "default": entry.get("isDefault") is True})
        if not catalog:
            raise failure(provider, {"message": "empty model catalog"})
        return {"source": "provider_rpc", "models": catalog}


def parse_action(provider, text):
    try:
        return validate(json.loads(text))
    except (ValueError, TypeError):
        raise Failure({"status": "unknown", "scope": "model", "reason": "invalid_action"}) from None


def request(provider, model, credential, prompt, effort="medium", timeout=180):
    with isolated(provider, credential, timeout) as (root, env, rpc):
        if provider == "claude":
            command = ["claude", "-p", prompt, "--model", model, "--effort", effort,
                       "--tools", "", "--max-turns", "1", "--output-format", "json",
                       "--setting-sources", "", "--strict-mcp-config", "--mcp-config", str(root / "mcp.json"),
                       "--json-schema", json.dumps(ACTION_SCHEMA)]
            result = subprocess.run(sandbox(command, root), cwd=root, env=env, stdin=subprocess.DEVNULL,
                                    capture_output=True, text=True, timeout=timeout)
            try:
                output = json.loads(result.stdout)
            except ValueError:
                raise failure(provider, result.stdout + result.stderr) from None
            if result.returncode or output.get("is_error"):
                raise failure(provider, output)
            structured = output.get("structured_output")
            return validate(structured) if isinstance(structured, dict) else parse_action(provider, output.get("result", ""))
        if provider == "codex":
            started = checked(provider, rpc.call("thread/start", {"model": model, "cwd": str(root),
                                      "approvalPolicy": "never", "sandbox": "read-only", "ephemeral": True}))
            thread = started["thread"]["id"]
            checked(provider, rpc.call("turn/start", {"threadId": thread, "model": model, "effort": effort,
                     "approvalPolicy": "never", "input": [{"type": "text", "text": prompt}],
                     "outputSchema": ACTION_SCHEMA}))
        else:
            started = checked(provider, rpc.call("session.create", {"model": model, "availableTools": [], "tools": [],
                      "excludedTools": [], "requestPermission": False, "requestUserInput": False,
                      "hooks": False, "workingDirectory": str(root), "streaming": False}))
            thread = started["sessionId"]
            checked(provider, rpc.call("session.send", {"sessionId": thread, "prompt": prompt,
                      "responseFormat": {"type": "json_schema", "jsonSchema": {
                          "name": "action", "strict": True, "schema": ACTION_SCHEMA}}}))
        answer = None
        pending, rpc.notifications = rpc.notifications, []
        while True:
            event = pending.pop(0) if pending else rpc.receive()
            if not isinstance(event, dict):
                continue
            if "method" in event and "id" in event:
                # No native tool permission, user interaction or token refresh
                # callback may cross the boundary. End instead of granting it.
                raise Failure({"status": "unknown", "scope": "model", "reason": "native_request_denied"})
            params = event.get("params") or {}
            method = event.get("method")
            if provider == "codex":
                if method == "item/completed":
                    item = params.get("item", {})
                    if item.get("type") == "agentMessage":
                        answer = item.get("text")
                if method == "turn/completed":
                    turn = params.get("turn", {})
                    if turn.get("status") != "completed":
                        raise failure(provider, turn)
                    break
            elif method == "session.event" and params.get("sessionId") == thread:
                item = params.get("event") or {}
                kind, data = item.get("type"), item.get("data", {})
                if kind == "assistant.message":
                    if data.get("toolRequests"):
                        raise Failure({"status": "unknown", "scope": "model", "reason": "native_request_denied"})
                    answer = data.get("content")
                if kind in {"session.error", "tool.execution_start"}:
                    raise failure(provider, data)
                if kind == "session.idle":
                    break
        return parse_action(provider, answer or "")
