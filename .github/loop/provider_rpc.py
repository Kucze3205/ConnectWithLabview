"""Bounded JSON-RPC transport. Provider diagnostics never become engine logs."""
import json
import queue
import subprocess
import threading
import time


class RPC:
    def __init__(self, command, *, cwd, env, timeout=90, framing="lines"):
        self.command, self.cwd, self.env = command, cwd, env
        self.deadline = time.monotonic() + timeout
        self.framing = framing
        self.events, self.notifications = queue.Queue(), []
        self.sequence = 0

    def __enter__(self):
        self.process = subprocess.Popen(self.command, cwd=self.cwd, env=self.env, stdin=subprocess.PIPE,
                                        stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        self.reader = threading.Thread(target=self._read, daemon=True)
        self.reader.start()
        return self

    def _read(self):
        try:
            while True:
                line = self.process.stdout.readline(16_000_001)
                if not line:
                    break
                if len(line) > 16_000_000:
                    raise ValueError('provider frame exceeds limit')
                if self.framing == "headers":
                    if not line.lower().startswith(b"content-length:"):
                        continue
                    length = int(line.split(b":", 1)[1])
                    if not 0 < length <= 16_000_000:
                        raise ValueError("invalid provider frame size")
                    while self.process.stdout.readline().strip():
                        pass
                    line = self.process.stdout.read(length)
                try:
                    self.events.put(json.loads(line))
                except ValueError:
                    continue
        except (OSError, ValueError):
            pass
        finally:
            self.events.put(None)

    def send(self, method, params=None, identifier=None):
        message = {"method": method}
        if params is not None:
            message["params"] = params
        if identifier is not None:
            message["id"] = identifier
        if self.framing == "headers":
            message["jsonrpc"] = "2.0"
        self.write(message)

    def respond(self, identifier, result=None):
        message = {"id": identifier, "result": result}
        if self.framing == "headers":
            message["jsonrpc"] = "2.0"
        self.write(message)

    def write(self, message):
        encoded = json.dumps(message).encode()
        frame = b"Content-Length: %d\r\n\r\n" % len(encoded) + encoded if self.framing == "headers" else encoded + b"\n"
        self.process.stdin.write(frame)
        self.process.stdin.flush()

    def receive(self):
        remaining = self.deadline - time.monotonic()
        if remaining <= 0:
            raise TimeoutError("provider RPC timed out")
        try:
            value = self.events.get(timeout=remaining)
        except queue.Empty as exc:
            raise TimeoutError("provider RPC timed out") from exc
        if value is None:
            raise RuntimeError("provider RPC disconnected")
        return value

    def call(self, method, params=None):
        self.sequence += 1
        identifier = self.sequence
        self.send(method, params, identifier)
        while True:
            event = self.receive()
            if isinstance(event, dict) and event.get("id") == identifier:
                if "error" in event:
                    # Caller may classify the error in memory. Never stringify it
                    # into an exception that could print account/token data.
                    return {"rpc_error": event["error"]}
                return event.get("result")
            self.notifications.append(event)

    def __exit__(self, *exc):
        self.process.terminate()
        try:
            self.process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            self.process.kill()
            self.process.wait(timeout=5)
        self.reader.join(timeout=1)
        self.process.stdin.close()
        self.process.stdout.close()
