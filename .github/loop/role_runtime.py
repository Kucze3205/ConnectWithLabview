"""Trusted action loop with provider fallback and durable turn checkpoints.

The transport never sees the checkout. The broker never sees credentials. A
tool action becomes accepted only after its files and continuation are remote.
"""
import hashlib
import json
import os
import subprocess
import time
from datetime import datetime, timedelta, timezone

import provider_pool as pool
from provider_adapter import Failure, request
from tool_broker import ACTION_SCHEMA, validate


def now():
    return datetime.now(timezone.utc)


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


class Runtime:
    def __init__(self, owner, policy, task, store, session_key, broker, checkpoint,
                 credentials, prompt, fingerprint, effort="medium", model_request=request, clock=now):
        self.owner, self.policy, self.task = owner, policy, task
        self.store, self.key, self.broker, self.checkpoint = store, session_key, broker, checkpoint
        self.credentials, self.prompt, self.fingerprint = credentials, prompt, fingerprint
        self.effort, self.request, self.clock = effort, model_request, clock

    def availability(self):
        identities = {provider: hashlib.sha256(value.encode()).hexdigest()
                      for provider, value in self.credentials.items()}
        def changed(document):
            state = document.setdefault("availability", {})
            previous = document.setdefault("credentials", {})
            for provider, identity in identities.items():
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

    def observe(self, candidate, result, observed):
        def change(document):
            document["availability"] = pool.record_outcome(
                self.owner, document.get("availability", {}), **candidate,
                status=result["status"], now=observed, scope=result.get("scope", "model"),
                retry_after=result.get("retry_after"))
            return document
        self.store.update("pool.json", change)

    def save(self, state, files=False):
        if files:
            state = dict(state, **self.checkpoint(state))
        self.store.update(self.key, lambda _: state)
        return state

    def run(self, max_turns, seconds):
        state = self.store.read(self.key)
        if state.get("fingerprint") != self.fingerprint:
            state = {"fingerprint": self.fingerprint, "turns": 0, "history": []}
        elif state.get("pending"):
            state["history"].append({"recovery": "The runner stopped with this action pending. It may have run. "
                                     "Inspect the current files before proposing another operation.",
                                     "action": state.pop("pending")})
        state.pop("result", None)
        state = self.save(state)
        deadline = time.monotonic() + seconds
        for _ in range(max_turns):
            remaining = deadline - time.monotonic()
            if remaining < 5:
                break
            choice = pool.select_candidate(self.owner, self.policy, self.availability(), self.task, self.clock())
            if choice["action"] in {"wait", "blocked"}:
                result = {"status": "paused", "reason": "providers_unavailable", **choice}
                # Authentication also waits for new credentials; the watchdog
                # rechecks with bounded delay without exhausting old park counts.
                result.setdefault("retry_after", pool._iso(self.clock() + timedelta(
                    seconds=self.owner["backoff"]["max_seconds"])))
                self.save(dict(state, result=result), files=True)
                return result
            candidate = choice["candidate"]
            observed = self.clock()
            provider = candidate["provider"]
            prompt = (self.prompt + '\n\nYou propose one JSON action matching this schema: ' +
                      json.dumps(ACTION_SCHEMA) + '\nUse no native tools. All role tools are executed by the parent. '
                      'The parent commits accepted changes. Read staged skills instead of calling a native Skill tool. '
                      'Commands are argv strings, without shell expansion. Unused fields must be empty strings. '
                      'Finish only after writing the required report and outputs.\nRecent continuation:\n' +
                      json.dumps(state["history"], ensure_ascii=False))
            if hasattr(self.broker, 'profile'):
                prompt += '\nRole profile: ' + json.dumps(self.broker.profile)
            if getattr(self.broker, 'resources', None):
                prompt += ('\nPrepared public sources are read-only under @environment/ in Read/Glob/Grep. '
                           'Commands see them through LABVIEW_ENVIRONMENT=/resources/environment.')
            credential = self.credentials.get(provider, "")
            try:
                if not credential:
                    raise Failure({"status": "auth_failure", "scope": "provider", "reason": "missing_secret"})
                action = validate(self.request(provider, candidate["model"], credential, prompt,
                                               effort=self.effort, timeout=min(180, remaining)))
            except Failure as error:
                self.observe(candidate, error.observation, observed)
                continue
            except (OSError, ValueError, TypeError, RuntimeError, subprocess.SubprocessError):
                self.observe(candidate, {"status": "unknown", "scope": "provider"}, observed)
                continue
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
            # Files are the durable source of truth; keep a bounded recent
            # conversation, instructing recovery to inspect earlier file work.
            while len(json.dumps(state["history"])) > 600_000 and len(state["history"]) > 1:
                state["history"].pop(0)
            state = self.save(state, files=True)
            if action["tool"] == "Finish" and "error" not in outcome:
                result = {"status": outcome["status"], "candidate": candidate, "turns": state["turns"]}
                self.save(dict(state, result=result))
                return result
        result = {"status": "partial", "reason": "session_budget", "turns": state["turns"]}
        self.save(dict(state, result=result), files=True)
        return result
