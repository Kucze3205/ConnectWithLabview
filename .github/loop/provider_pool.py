"""Deterministic routing policy; adapters must perform probes and persist outcomes.

Owner config supplies providers/models and bounded backoff. Policy supplies ordered
``tasks[task]`` candidate lists. No task or model has an implicit fallback.
"""
from datetime import datetime, timedelta, timezone
import copy
import re


TRANSIENT = {"quota", "unknown", "throttled", "network_failure", "service_failure", "credential_expired"}
PERMANENT = {"auth_failure", "entitlement_failure"}
STATUSES = {"available"} | TRANSIENT | PERMANENT


def _time(value, name="now"):
    if isinstance(value, str):
        try:
            value = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError as exc:
            raise ValueError(name + " must be an ISO timestamp with timezone") from exc
    if not isinstance(value, datetime) or value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(name + " must have a timezone")
    return value.astimezone(timezone.utc)


def _iso(value):
    return value.isoformat().replace("+00:00", "Z")


def _config(owner):
    if not isinstance(owner, dict) or not isinstance(owner.get("providers"), dict) or not owner["providers"]:
        raise ValueError("owner.providers must be a nonempty model catalog")
    for provider, entry in owner["providers"].items():
        if not isinstance(provider, str) or not provider or not isinstance(entry, dict):
            raise ValueError("invalid provider catalog entry")
        models = entry.get("models")
        if not isinstance(models, list) or not models or any(not isinstance(m, str) or not m for m in models):
            raise ValueError("provider models must be a nonempty string list")
        if len(set(models)) != len(models):
            raise ValueError("provider models must be unique")
    backoff = owner.get("backoff")
    if not isinstance(backoff, dict):
        raise ValueError("owner.backoff is required")
    initial, maximum = backoff.get("initial_seconds"), backoff.get("max_seconds")
    if type(initial) is not int or type(maximum) is not int or not 0 < initial <= maximum:
        raise ValueError("backoff requires positive integer initial_seconds <= max_seconds")
    return initial, maximum


def _candidate(owner, candidate):
    if not isinstance(candidate, dict) or set(candidate) != {"provider", "model"}:
        raise ValueError("candidate requires only provider and model")
    provider, model = candidate["provider"], candidate["model"]
    if not isinstance(provider, str) or not isinstance(model, str):
        raise ValueError("candidate provider and model must be strings")
    if provider not in owner["providers"] or model not in owner["providers"][provider]["models"]:
        raise ValueError("candidate is outside the owner's allowed model catalog")


def _delay(owner, attempts):
    initial, maximum = _config(owner)
    # Saturate before exponentiation, including maliciously large persisted counts.
    return min(maximum, initial * 2 ** min(attempts - 1, maximum.bit_length()))


def _error(error):
    """Sanitized failure of our own side: the exception class and errno, never its text or argv."""
    if (not isinstance(error, dict) or set(error) - {"type", "errno"} or not isinstance(error.get("type"), str)
            or not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]{0,63}", error["type"])
            or "errno" in error and type(error["errno"]) is not int):
        raise ValueError("invalid availability error")
    return error


def _record(owner, record):
    if not isinstance(record, dict) or set(record) - {"status", "observed_at", "retry_after", "attempts", "error"}:
        raise ValueError("invalid availability record")
    if "error" in record:
        _error(record["error"])
    if not isinstance(record.get("status"), str) or record["status"] not in STATUSES:
        raise ValueError("invalid availability status")
    attempts = record.get("attempts", 1)
    if type(attempts) is not int or attempts < 1:
        raise ValueError("availability attempts must be a positive integer")
    observed = _time(record.get("observed_at"), "observed_at")
    retry = record.get("retry_after")
    if retry is not None:
        retry = _time(retry, "retry_after")
        if retry <= observed:
            raise ValueError("retry_after must follow observed_at")
    if record["status"] in {"available"} | PERMANENT:
        if retry is not None:
            raise ValueError("available or permanent failures cannot have retry_after")
        return None
    return retry if retry is not None else observed + timedelta(seconds=_delay(owner, attempts))


def _state(owner, state):
    if not isinstance(state, dict) or set(state) - {"providers", "models"}:
        raise ValueError("state supports only providers and models")
    for scope in ("providers", "models"):
        entries = state.get(scope, {})
        if not isinstance(entries, dict):
            raise ValueError("state scope must be a mapping")
        for provider, value in entries.items():
            if provider not in owner["providers"]:
                raise ValueError("state contains an unconfigured provider")
            if scope == "providers":
                _record(owner, value)
            else:
                if not isinstance(value, dict):
                    raise ValueError("model state must be a mapping")
                for model, record in value.items():
                    _candidate(owner, {"provider": provider, "model": model})
                    _record(owner, record)


def select_candidate(owner, policy, state, task, now):
    """Return JSON-safe run/probe/wait/blocked without mutating any input.

    A missing model record needs a probe. Provider records impose an additional
    restriction on every model. Expired quotas require a probe, never imply
    availability. Authentication failures remain blocked until explicitly updated.
    """
    _config(owner)
    _state(owner, state)
    now = _time(now)
    if not isinstance(policy, dict) or not isinstance(policy.get("tasks"), dict):
        raise ValueError("policy.tasks must be a mapping")
    for name, candidates in policy["tasks"].items():
        if not isinstance(name, str) or not name or not isinstance(candidates, list) or not candidates:
            raise ValueError("each task requires a nonempty ordered candidate list")
        for candidate in candidates:
            _candidate(owner, candidate)
    if task not in policy["tasks"]:
        raise ValueError("task has no explicit routing policy")
    reasons, retries = [], []
    for candidate in policy["tasks"][task]:
        provider, model = candidate["provider"], candidate["model"]
        records = [
            ("provider", state.get("providers", {}).get(provider)),
            ("model", state.get("models", {}).get(provider, {}).get(model)),
        ]
        blocked, blocked_statuses, waits, probe_scope, errors = [], [], [], None, []
        for scope, record in records:
            if record is None:
                if scope == "model":
                    probe_scope = probe_scope or scope
                continue
            status = record["status"]
            if status in PERMANENT:
                blocked.append(scope)
                blocked_statuses.append(status)
            elif status in TRANSIENT:
                retry = _record(owner, record)
                if retry > now:
                    waits.append(retry)
                    errors += [record["error"]] if "error" in record else []
                else:
                    probe_scope = probe_scope or scope
        if blocked:
            reasons.append(dict(candidate, reason=blocked_statuses[0], scopes=blocked))
        elif waits:
            # Both model and provider restrictions must expire for this candidate.
            retry = max(waits)
            retries.append(retry)
            reasons.append(dict(candidate, reason="cooldown", retry_after=_iso(retry), **({"error": errors[0]} if errors else {})))
        else:
            result = {"action": "probe" if probe_scope else "run", "candidate": dict(candidate), "reasons": reasons}
            if probe_scope:
                result["scope"] = probe_scope
            return result
    if retries:
        return {"action": "wait", "retry_after": _iso(min(retries)), "reasons": reasons}
    reason = "authentication_required" if any(r["reason"] == "auth_failure" for r in reasons) else "model_entitlement_required"
    return {"action": "blocked", "reason": reason, "reasons": reasons}


def record_outcome(owner, state, provider, model, status, now, retry_after=None, scope="model", error=None):
    """Return a copied state with an adapter observation and bounded retry delay.

    Adapters must explicitly report whether exhaustion covers a model or provider.
    Only a real available observation clears a failure; time alone never clears it.
    """
    _config(owner)
    _state(owner, state)
    _candidate(owner, {"provider": provider, "model": model})
    if not isinstance(scope, str) or scope not in {"provider", "model"} or not isinstance(status, str) or status not in STATUSES:
        raise ValueError("invalid outcome scope or status")
    now = _time(now)
    result = copy.deepcopy(state)
    providers = result.setdefault("providers", {})
    models = result.setdefault("models", {})
    target = providers if scope == "provider" else models.setdefault(provider, {})
    key = provider if scope == "provider" else model
    previous = target.get(key, {})
    if previous and _time(previous["observed_at"]) > now:
        return result  # a late writer must not replace a newer observation
    attempts = previous.get("attempts", 0) + 1 if previous.get("status") == status and status in TRANSIENT else 1
    record = {"status": status, "observed_at": _iso(now), "attempts": attempts}
    if retry_after is not None:
        retry = _time(retry_after, "retry_after")
        if status not in TRANSIENT or retry <= now:
            raise ValueError("retry_after requires quota/unknown and a future timestamp")
        record["retry_after"] = _iso(retry)
    elif status in TRANSIENT:
        record["retry_after"] = _iso(now + timedelta(seconds=_delay(owner, attempts)))
    if error is not None:
        record["error"] = _error(error)
    target[key] = record
    return result
