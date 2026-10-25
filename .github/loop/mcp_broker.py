#!/usr/bin/env python3
"""MCP stdio server inside the model boundary: a single Bash tool forwarded to the trusted broker.

The command never runs here. It goes over a Unix socket to `tool_broker.Broker` outside the boundary,
which applies the role's Bash rules and runs it in its own bubblewrap. Standard library only.
"""
import json
import socket
import sys

SOCKET = "/engine/broker.sock"
TOOL = {"name": "Bash",
        "description": "Run one command (no shell syntax: no pipes, &&, redirects or cd) in the role workspace. "
                       "Only the role's permitted commands run; the workspace root is read-only except the "
                       "paths the role may write.",
        "inputSchema": {"type": "object", "properties": {"command": {"type": "string"}},
                        "required": ["command"], "additionalProperties": False}}


def forward(command):
    with socket.socket(socket.AF_UNIX) as connection:
        connection.connect(SOCKET)
        connection.sendall(json.dumps({"command": command}).encode() + b"\n")
        connection.shutdown(socket.SHUT_WR)
        data = b""
        while chunk := connection.recv(65536):
            data += chunk
    return json.loads(data)


def call(arguments):
    command = arguments.get("command") if isinstance(arguments, dict) else None
    if not isinstance(command, str):
        return {"content": [{"type": "text", "text": "command must be a string"}], "isError": True}
    try:
        reply = forward(command)
    except (OSError, ValueError) as error:
        return {"content": [{"type": "text", "text": "broker unavailable: " + str(error)}], "isError": True}
    if "error" in reply:
        return {"content": [{"type": "text", "text": reply["error"]}], "isError": True}
    result = reply["ok"]
    text = result.get("text", "") + ("\n[output truncated]" if result.get("truncated") else "")
    return {"content": [{"type": "text", "text": "exit %s\n%s" % (result.get("exit"), text)}],
            "isError": result.get("exit") != 0}


def handle(message):
    method, ident = message.get("method"), message.get("id")
    if ident is None:
        return None  # notifications need no reply
    if method == "initialize":
        result = {"protocolVersion": message.get("params", {}).get("protocolVersion", "2025-03-26"),
                  "capabilities": {"tools": {}}, "serverInfo": {"name": "broker", "version": "1"}}
    elif method == "tools/list":
        result = {"tools": [TOOL]}
    elif method == "tools/call":
        params = message.get("params", {})
        if params.get("name") != "Bash":
            return {"jsonrpc": "2.0", "id": ident, "error": {"code": -32602, "message": "unknown tool"}}
        result = call(params.get("arguments"))
    elif method == "ping":
        result = {}
    else:
        return {"jsonrpc": "2.0", "id": ident, "error": {"code": -32601, "message": "method not found"}}
    return {"jsonrpc": "2.0", "id": ident, "result": result}


def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            reply = handle(json.loads(line))
        except ValueError:
            continue
        if reply is not None:
            sys.stdout.write(json.dumps(reply) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
