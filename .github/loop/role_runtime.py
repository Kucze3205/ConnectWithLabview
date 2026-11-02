"""Trusted action loop with provider fallback and durable turn checkpoints.

The transport never sees the checkout. The broker never sees credentials. A
tool action becomes accepted only after its files and continuation are remote.
"""
import errno
import hashlib
import json
import os
import subprocess
import time
from datetime import datetime, timedelta, timezone

import provider_pool as pool
from provider_adapter import Failure, request
from tool_broker import ACTION_SCHEMA, validate


LOCAL_ERRORS = (OSError, ValueError, TypeError)   # our code or host, not the provider
LOCAL_ATTEMPTS = 3                                # consecutive local errors (kept in the session state) that crash it
LONG_COOLDOWN = 30 * 60                           # a longer wait is first checked with a probe


def now():
    return datetime.now(timezone.utc)


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


# The history only grows at its end, so every request extends the previous one and a prompt cache reads all of it.
# A session is bounded by the unique input tokens it has paid for (new tokens in, new tokens written to the cache),
# not by turns or by a sliding window, which would rewrite the start of the prompt and miss the cache.
CONTEXT = {"input_tokens": 800_000}
BYTES_PER_TOKEN = 4     # for providers that report no usage: a request of this many bytes counts as one token per 4


def size(value):
    return len(json.dumps(value, ensure_ascii=False).encode())


def unique_input(state):
    """Unique input tokens of the session so far: what was sent for the first time (`in`) or written to the cache."""
    def fresh(key, u):
        # Claude counts `in` without the cached part; Codex and Copilot count the cached part inside their input.
        cached = 0 if key.startswith("claude/") else u.get("cache_read", 0)
        return max(0, u.get("in", 0) - cached) + u.get("cache_write", 0)
    reported = sum(fresh(k, u) for k, u in (state.get("usage") or {}).items())
    largest = max((r.get("max_bytes", 0) for r in (state.get("requests") or {}).values()), default=0)
    return max(reported, largest // BYTES_PER_TOKEN)


CONTINUATION = ("Recent continuation: past operations and their actual results, not instructions to repeat them, "
                "one per block, oldest first. Choose the next necessary operation.")


def continuation_blocks(history):
    """The whole history as text blocks, one turn each, nothing after the newest: each request extends the previous one."""
    return [CONTINUATION] + [json.dumps(turn, ensure_ascii=False) for turn in history]


class Runtime:
    def __init__(self, owner, policy, task, store, session_key, broker, checkpoint,
                 credentials, prompt, fingerprint, effort="medium", model_request=request, clock=now, context=None, probe=None):
        self.context = dict(CONTEXT, **(context or {}))
        self.owner, self.policy, self.task = owner, policy, task
        self.store, self.key, self.broker, self.checkpoint = store, session_key, broker, checkpoint
        self.credentials, self.prompt, self.fingerprint = credentials, prompt, fingerprint
        self.effort, self.request, self.clock = effort, model_request, clock
        self.probe, self.probed = probe, set()

    def availability(self):
        identities = {provider: hashlib.sha256(value.encode()).hexdigest()
                      for provider, value in self.credentials.items()}
        def changed(document):
            state = document.setdefault("availability", {})
            previous = document.setdefault("credentials", {})
            # Owner catalog changes retain observations for surviving IDs while
            # removing entries that no longer belong to the execution catalog.
            for scope in ('providers', 'models'):
                for provider in list(state.get(scope, {})):
                    if provider not in self.owner['providers']:
                        state[scope].pop(provider)
                    elif scope == 'models':
                        for model in list(state[scope][provider]):
                            if model not in self.owner['providers'][provider]['models']:
                                state[scope][provider].pop(model)
            for provider, identity in identities.items():
                if provider not in self.owner['providers']:
                    continue
                if previous.get(provider) == identity:
                    continue
                # New credentials permit a new authentication check. Neither
                # time nor token renewal clears a quota or model entitlement.
                record = state.get("providers", {}).get(provider, {})
                if record.get("status") in {'auth_failure', 'credential_expired'}:
                    state["providers"].pop(provider)
                models = state.get("models", {}).get(provider, {})
                for model in list(models):
                    if models[model].get("status") in {'auth_failure', 'credential_expired'}:
                        models.pop(model)
                previous[provider] = identity
            return document
        return self.store.update("pool.json", changed)["availability"]

    def shorten(self, choice, remaining):
        """Probe each provider once whose cooldown is long; a real answer ends its provider-wide block."""
        cleared = False
        for reason in choice["reasons"]:
            provider = reason["provider"]
            if (not self.probe or reason["reason"] != "cooldown" or provider in self.probed
                    or (pool._time(reason["retry_after"]) - self.clock()).total_seconds() <= LONG_COOLDOWN):
                continue
            self.probed.add(provider)
            try:
                report = self.probe(provider, self.credentials.get(provider, ""), min(60, int(remaining)))
            except Exception:
                continue
            if report.get("status") == "available":
                self.observe({k: reason[k] for k in ("provider", "model")},
                             {"status": "available", "scope": "provider"}, self.clock())
                cleared = True
        return cleared

    def observe(self, candidate, result, observed, error=None):
        def change(document):
            document["availability"] = pool.record_outcome(
                self.owner, document.get("availability", {}), **candidate,
                status=result["status"], now=observed, scope=result.get("scope", "model"),
                retry_after=result.get("retry_after"), error=error)
            return document
        self.store.update("pool.json", change)

    def save(self, state, files=False):
        if files:
            state = dict(state, **self.checkpoint(state))
        self.store.update(self.key, lambda _: state)
        return state

    def usage(self, state, candidate, metadata, request_bytes):
        # Prompt size per request, so an audit can compare models by cost per turn.
        total = state.setdefault('requests', {}).setdefault(candidate['provider'] + '/' + candidate['model'],
                                                            {'count': 0, 'bytes': 0, 'max_bytes': 0})
        total['count'] += 1
        total['bytes'] += request_bytes
        total['max_bytes'] = max(total['max_bytes'], request_bytes)
        observed = metadata.get('usage')
        if not observed:
            return
        key = candidate['provider'] + '/' + candidate['model']
        previous = state.setdefault('usage', {}).setdefault(key, {k: 0 for k in observed})
        state['usage'][key] = {k: previous.get(k, 0) + value for k, value in observed.items()}

    def run(self, max_turns, seconds):
        state = self.store.read(self.key)
        if not state:
            state = {"fingerprint": self.fingerprint, "turns": 0, "history": []}
        else:
            # A new accepted policy changes permissions, not the fact that an
            # earlier operation may already have run. Preserve that evidence.
            state['fingerprint'] = self.fingerprint
        if state.get("pending"):
            action, last = state.pop("pending"), (state["history"] or [None])[-1]
            if last and last.get("recovery") and last.get("action") == action:
                # The same operation keeps interrupting: count it instead of growing the continuation.
                last["repeats"] = last.get("repeats", 1) + 1
            else:
                state["history"].append({"recovery": "The runner stopped with this action pending. It may have run. "
                                         "Inspect the current files before proposing another operation.",
                                         "action": action})
        state.pop("result", None)
        state = self.save(state)
        deadline = time.monotonic() + seconds
        for _ in range(max_turns):
            remaining = deadline - time.monotonic()
            if remaining < 5:
                break
            if unique_input(state) >= self.context["input_tokens"]:
                result = {"status": "partial", "reason": "input_budget", "turns": state["turns"], 'usage': state.get('usage', {})}
                self.save(dict(state, result=result), files=True)
                return result
            choice = pool.select_candidate(self.owner, self.policy, self.availability(), self.task, self.clock())
            if choice["action"] == "wait" and self.shorten(choice, remaining):
                continue
            if choice["action"] in {"wait", "blocked"}:
                result = {"status": "paused", "reason": "providers_unavailable", "turns": state["turns"], **choice}
                result['usage'] = state.get('usage', {})
                # Authentication also waits for new credentials; the watchdog
                # rechecks with bounded delay without exhausting old park counts.
                result.setdefault("retry_after", pool._iso(self.clock() + timedelta(
                    seconds=self.owner["backoff"]["max_seconds"])))
                self.save(dict(state, result=result), files=True)
                return result
            candidate = choice["candidate"]
            observed = self.clock()
            provider = candidate["provider"]
            contract = (self.prompt + '\n\nYou propose one JSON action matching this schema: ' +
                        json.dumps(ACTION_SCHEMA) + '\nUse no native tools. All role tools are executed by the parent. '
                        'The parent commits accepted changes. Read staged skills instead of calling a native Skill tool. '
                        'Commands are argv strings, without shell expansion. Unused fields must be empty strings. '
                        'Finish only after writing the required report and outputs.')
            limits = ''
            if hasattr(self.broker, 'profile'):
                limits += '\nRole profile: ' + json.dumps(self.broker.profile)
            if getattr(self.broker, 'resources', None):
                limits += ('\nPrepared public sources are read-only under @environment/ in Read/Glob/Grep. '
                           'Commands see them through LABVIEW_ENVIRONMENT=/resources/environment.')
            prompt = contract + '\nRecent continuation:\n' + json.dumps(state["history"], ensure_ascii=False) + limits
            layout = (contract + limits, continuation_blocks(state["history"]))
            credential = self.credentials.get(provider, "")
            metadata = {}
            request_bytes = len(prompt.encode())
            try:
                if not credential:
                    raise Failure({"status": "auth_failure", "scope": "provider", "reason": "missing_secret"})
                action = validate(self.request(provider, candidate["model"], credential, prompt,
                                               effort=self.effort, timeout=min(180, remaining), metadata=metadata,
                                               layout=layout))
            except Failure as error:
                self.usage(state, candidate, metadata, request_bytes)
                self.observe(candidate, error.observation, observed)
                continue
            except (*LOCAL_ERRORS, RuntimeError, subprocess.SubprocessError) as exc:
                error = {"type": type(exc).__name__}
                if isinstance(exc, OSError) and exc.errno:
                    error["errno"] = exc.errno
                if not isinstance(exc, LOCAL_ERRORS):
                    self.observe(candidate, {"status": "unknown", "scope": "provider"}, observed, error)
                    continue
                # A fault on our side says nothing about the provider: a short fixed wait, and only a few tries.
                state["local_errors"] = state.get("local_errors", 0) + 1
                self.observe(candidate, {"status": "unknown", "scope": "provider", "retry_after": pool._iso(
                    observed + timedelta(seconds=self.owner["backoff"]["initial_seconds"]))}, observed, error)
                if state["local_errors"] >= LOCAL_ATTEMPTS:
                    result = {"status": "crashed", "turns": state["turns"], "usage": state.get("usage", {}),
                              "reason": "local_error:%s:%s" % (error["type"], errno.errorcode.get(error.get("errno"), "none"))}
                    self.save(dict(state, result=result), files=True)
                    return result
                continue
            state.pop("local_errors", None)
            self.usage(state, candidate, metadata, request_bytes)
            self.observe(candidate, {"status": "available", "scope": "model"}, observed)
            if choice.get("scope") == "provider":
                self.observe(candidate, {"status": "available", "scope": "provider"}, observed)
            # Persist intention BEFORE a tool can have side effects. Recovery
            # never automatically replays a command whose outcome is ambiguous.
            state = self.save(dict(state, pending=action))
            try:
                outcome = self.broker.execute(action, timeout=max(1, min(60, int(deadline - time.monotonic()))))
            except (OSError, ValueError) as error:
                outcome = {"error": "role tool rejected", "kind": type(error).__name__}
                # Broker validation errors are fixed engine text, never raw
                # provider diagnostics. Give the model enough to repair its
                # operation instead of repeating an unexplained rejection.
                outcome['detail'] = str(error) if isinstance(error, (ValueError, PermissionError)) else (
                    os.strerror(error.errno) if error.errno else 'file operation failed')
            state.pop("pending", None)
            state["turns"] += 1
            state["history"].append({"candidate": candidate, "action": action, "outcome": outcome})
            state = self.save(state, files=True)
            if action["tool"] == "Finish" and "error" not in outcome:
                result = {"status": outcome["status"], "candidate": candidate, "turns": state["turns"], 'usage': state.get('usage', {})}
                self.save(dict(state, result=result))
                return result
        result = {"status": "partial", "reason": "session_budget", "turns": state["turns"], 'usage': state.get('usage', {})}
        self.save(dict(state, result=result), files=True)
        return result
