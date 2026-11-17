"""The end of a session: the epilogue takes its results, merges or parks it, and closes it.
"""
import json
import os
import re
import shutil
import tarfile
import tempfile
import time
from datetime import timedelta

import agent_result
import artifact_pin
import check_results
import closing
import common as c
import iteration as it
import merge
import owner_requests as requests
import policy_apply
import policy_inputs
import policymaker_session
import release_assets
import session_artifact
import session_reports
import session_startup
import session_summary
import watchdog


def fix_round(n, f, upd, why):
    """A failed `## Verification` or `check` is an error the agent can fix: run the same issue again, its report carrying
    the error, up to the policy's `fix_rounds` times. False when the rounds are spent."""
    kk, max_fixes = int(f.get("fixes", 0)) + 1, c.limits()["fix_rounds"]
    if kk > max_fixes:
        return False
    upd["fixes"] = kk
    c.update_report(n, dict(upd, status="partial"), "%s\nCorrection round %s of %s." % (why, kk, max_fixes))
    c.launch(n)
    return True


def finalize(n, work):
    tmp = os.environ.get("RUNNER_TEMP", tempfile.gettempdir())
    i = c.issue(n)
    labels = c.label_names(i)
    role = c.roles_of(labels)[0]
    k = c.iteration_of(labels) or 0
    p = policymaker_session.profile_of(role) or {}
    script = p.get("agent") is False
    routed = bool(c.cfg().get("provider_pool")) and not script
    text = c.safe_read(work, ".session/report.md")
    if text:
        c.publish(n, text)
    f = c.report_fields(n)
    status = f.get("status", "")
    exit_code = ""
    if os.path.exists(os.path.join(tmp, "agent-exit")):
        with open(os.path.join(tmp, "agent-exit")) as fh:
            exit_code = fh.read().strip()
    missing = (c.safe_read(tmp, "secret-missing") or "").strip()
    if missing and re.fullmatch(r"[A-Z][A-Z0-9_]*", missing) and missing in requests.secrets_of_consent(labels, n, p):
        closing.block_secret_missing(n, i, missing, work)
        return
    exec_path = os.path.join(tmp, "claude-execution-output.json")
    limited, reset, prose = False, None, ""
    upd = {"branch": "task/%s" % n, "iteration": k, "runner": os.environ.get("RUNNER_OS") or None, "stage_failures": None}
    if script:
        upd["cause"] = "exit=%s" % exit_code if exit_code not in ("0", "") else None
        status = "done" if exit_code == "0" else "crashed"
        prose = "Script %s.\n" % ("finished" if status == "done" else "failed (exit %s)" % exit_code) + (c.safe_read(tmp, "script-output.txt") or "")[-1500:]
    elif routed:
        try:
            with open(os.path.join(tmp, "provider-execution-output.json"), encoding="utf-8") as fh:
                execution = json.load(fh)
        except (OSError, ValueError):
            execution = {}
        if not execution:
            # A killed runner may leave no summary, despite a durable action
            # intent/commit. Recover that session rather than closing its issue.
            try:
                from runtime_store import GitHubBackend, Store
                checkpoint = Store(GitHubBackend(c.REPO, base=c.default_branch())).read("sessions/%s.json" % n)
                if checkpoint:
                    execution = {"status": "paused", "reason": "execution_summary_missing",
                                 "retry_after": c.iso(c.now() + timedelta(seconds=c.cfg()["provider_pool"]["backoff"]["initial_seconds"]))}
            except Exception:
                execution = {"status": "paused", "reason": "checkpoint_store_unavailable",
                             "retry_after": c.iso(c.now() + timedelta(seconds=c.cfg()["provider_pool"]["backoff"]["initial_seconds"]))}
        status = execution.get("status")
        if status not in c.AGENT_STATUSES | {"paused"}:
            status = "crashed"
        limited = status == "paused"
        reset = c.parse_time(execution["retry_after"]) if execution.get("retry_after") else None
        reason = execution.get("reason")
        upd.update(cause=("providers:unavailable" if reason == "providers_unavailable" else "runtime:" + str(reason)) if limited else reason,
                   model=(execution.get("candidate") or {}).get("model"), effort=os.environ.get("EFFORT"),
                   turns=execution.get("turns"))
        per = execution.get('usage') or {}
        if per:
            upd.update(models=json.dumps(per, separators=(',', ':'), sort_keys=True),
                       tokens_in=sum(v.get('in', 0) for v in per.values()),
                       tokens_out=sum(v.get('out', 0) for v in per.values()),
                       cache_read=sum(v.get('cache_read', 0) for v in per.values()),
                       cache_write=sum(v.get('cache_write', 0) for v in per.values()))
        prose = (("All policy candidates are unavailable; durable checkpoint retained for resume."
                  if reason == "providers_unavailable" else "Trusted execution was interrupted; resume will inspect the durable checkpoint.")
                 if limited else "")
    else:
        cause, limited, reset = agent_result.machine_cause(exec_path, exit_code)
        if limited and status not in c.AGENT_STATUSES:
            # the status files are the session's data: only the engine's own probe parks the loop, and it sets the clock
            limited, reset = c.probe_limit()
        upd["cause"] = cause or None
        upd.update(agent_result.usage_fields(exec_path))
        upd.update(model=os.environ.get("MODEL") or None, effort=os.environ.get("EFFORT") or None)
        if status not in c.AGENT_STATUSES:
            status = "paused" if limited else "crashed"
            prose = "Subscription limit; resume scheduled." if limited else "The agent left no terminal status (%s)." % (cause or "no cause")
    a0, a1 = agent_result.read_int(os.path.join(tmp, "agent-start")), agent_result.read_int(os.path.join(tmp, "agent-end"))
    if a0 and a1:
        upd["agent_s"] = a1 - a0
    t0 = agent_result.read_int(os.path.join(tmp, "session-start"))
    if t0:
        upd["total_s"] = int(time.time()) - t0
        if f.get("paused_at"):
            upd["parked_s"] = int(f.get("parked_s", 0) or 0) + max(0, t0 - int(c.parse_time(f["paused_at"]).timestamp()))
            upd["paused_at"] = None
    sha, touched = merge.fetch_candidate(work, n)          # nothing on the branch dies with the runner
    if sha is None and status in ("done", "partial"):
        status, prose = "crashed", "The epilogue could not read the agent's repository, so nothing was kept."
    if touched and status in ("done", "partial"):
        status, prose, sha = "blocked", "The change touches protected paths: %s. The branch was not published and nothing was merged." % ", ".join(touched), None
        upd["merged"] = "false"
    if sha and status in c.AGENT_STATUSES | {"paused"}:
        upd["commit"] = sha if routed else f.get("commit", sha)
    if status != "paused":
        release_assets.upload_artifacts(n, work, k)
    if status == "done" and sha and not script:
        with merge.Tree("task/%s" % n) as cand:
            ok, out = merge.run_verification(cand, i["body"], n)
        if merge.verification_commands(i["body"]):
            upd["verification"] = "pass" if ok else "fail"
        if not ok:
            status, prose = "partial", "The epilogue ran `## Verification` and got an error:\n```\n%s\n```" % out
            if fix_round(n, f, upd, prose):
                return
    pending = None
    if status == "done" and sha and role == "policymaker":
        pending = "pending-iteration"            # its changes and orders take effect when the iteration it opened continues
        prose = policy_apply.hold_policymaker_output(n, work)
        c.edit_labels(n, add=["awaiting:iteration"])
        c.update_report(n, dict(upd, status="done", merged=pending), prose)
    elif status == "done" and sha:
        r = merge.merge_branch(n, role, i)
        upd["gate_s"] = r["gate_s"] or None
        if r["result"] == "conflict":
            kk = int(f.get("conflicts", 0)) + 1
            upd["conflicts"] = kk
            if kk < c.limits()["merge_conflict_retries"]:
                c.update_report(n, dict(upd, status="partial"), "Rebase on the default branch: conflict (attempt %s)." % kk)
                c.edit_labels(n, add=["conflict"])
                c.launch(n)
                return
            status, prose = "crashed", "Rebase conflict %s times in a row." % kk
        elif r["result"] == "awaiting-owner":
            pending = "pending-owner"
            req = requests.open_request("merge-acceptance", "Accept the change of task #%s: %s" % (n, i["title"]),
                                  "Task #%s finished; its branch `task/%s` (%s) is ready to enter the main line.\nFiles: %s" % (
                                      n, n, upd.get("commit", ""), ", ".join(r["changed"][:20])),
                                  "Every change needs a verdict before it enters the main line, and the change gate is set to you.",
                                  "Completed merges the branch; not planned discards it (the branch stays). Say why in a comment.",
                                  ref="task-%s" % n, iteration=k)
            c.edit_labels(n, add=["awaiting:owner"])
            c.update_report(n, dict(upd, status="done", merged=pending), "Waiting for the owner: request #%s." % req)
        elif r["result"] == "awaiting-verifier":
            pending = "pending-verifier"
            v = merge.request_verifier(n, i, k, r["changed"])
            c.edit_labels(n, add=["awaiting:verifier"])
            c.update_report(n, dict(upd, status="done", merged=pending), "The evaluator changed; waiting for the verifier (#%s)." % v)
        else:
            status, more, prose = merge.merge_outcome(r)
            upd.update(more)
            if r["result"] == "check" and fix_round(n, f, upd, prose):
                return
    elif status not in ("done", "paused") and sha and role != "policymaker":
        merge.merge_notes(n, role)
    if status == "paused":
        ended = watchdog.park(n, i, f, upd, prose, reset, sha, durable=routed)
        if ended is None:
            session_reports.capture(n, work)
            return
        status, prose = "crashed", ended
    if not pending:
        merge.tag_unmerged(n, k, upd)
    proposals(work, k, source=n)
    if pending:
        session_reports.capture(n, work)
    after_session(n, i, labels, role, k, work, status, upd, prose, pending)


def refuse_policy_results(n, why, rollback=True):
    """The policy scripts' job left bad results: the session did not start. Fails the iteration and rolls policy back, as for any
    policy script output the engine refuses. Not when the job left no result at all (`rollback=False`): that is GitHub's failure,
    and a rollback would also return the owner's own edits of `policy/` (this loop, 9-11 Nov 2026)."""
    k = c.iteration_of(c.label_names(c.issue(n)))
    if k is not None:
        it.fail_iteration(k, "invalid policy script output: %s" % why, rollback=rollback)
    raise SystemExit("invalid policy script output: %s" % why)


def note_startup_budget(n, policy_results):
    """The startup budget the policy scripts' job measured: the incident and the comment on the session's issue, which need the token."""
    budget = policy_inputs.budget(policy_results)
    if budget is None:
        return
    try:
        session_startup.record(n, c.roles_of(c.label_names(c.issue(n)))[0], budget)
    except (Exception, SystemExit):
        # Notification failures must never turn a diagnostic into a session gate.
        c.say("session #%s: startup notice could not be persisted" % n)


def epilogue(n, artifact, baseline, digest, policy_results):
    """The epilogue job, on a fresh runner: first the verdict of the policy scripts' job (`POLICY_OK`, `POLICY_ERROR`, `POLICY_DIGEST`
    and its artifact `policy_results`); then takes the session's results in (`receive`) and the results of "Check the results"
    only from that job's output (`CHECKS_RESULTS`, `check_results.accept`), and finalizes."""
    env = os.environ.get
    why = policy_inputs.refusal(env("POLICY_OK"), env("POLICY_ERROR"), policy_results, env("POLICY_DIGEST"))
    if why:
        refuse_policy_results(n, why, rollback=bool(env("POLICY_OK")))     # a job that never answered is GitHub's failure, not the policy's
    note_startup_budget(n, policy_results)
    tmp = os.environ.get("RUNNER_TEMP", tempfile.gettempdir())
    work = receive(n, artifact, baseline, digest, tmp)
    publish_runtime_state(n, tmp)
    check_results.accept(env("CHECKS_RESULTS"))
    try:
        finalize(n, work)
    finally:
        session_summary.write(n, os.environ.get("ROLE") or "session", work, tmp)


def publish_runtime_state(n, tmp):
    """A routed session's availability observations and continuation, left by the session job as data."""
    pool_cfg = c.cfg().get("provider_pool")
    if not pool_cfg:
        return
    from runtime_store import GitHubBackend, Store, publish
    values = []
    for name in ("runtime-pool.json", "runtime-session.json"):
        try:
            with open(os.path.join(tmp, name), encoding="utf-8") as fh:
                values.append(json.load(fh))
        except (OSError, ValueError):
            values.append(None)
    if not any(values):
        return
    try:
        publish(Store(GitHubBackend(c.REPO, base=c.default_branch())), pool_cfg, values[0], "sessions/%s.json" % n, values[1])
    except Exception as error:      # the session still closes; a lost observation only costs a probe
        print("runtime state not published: %s" % type(error).__name__)


def receive(n, artifact, baseline, digest, tmp):
    """The session job's artifact taken in as data (`session_artifact`), and the executor baseline from the channel the session
    cannot touch (`baseline/`, pinned by `digest`) put where admission reads it. Returns the tree; one that cannot be taken in
    is as good as no tree."""
    try:
        artifact_pin.verify(baseline, digest)
    except (OSError, ValueError):
        raise SystemExit("the executor baseline does not match the one staged")
    with open(os.path.join(baseline, "executor-baseline.json"), "rb") as fh:
        raw = fh.read()
    work = os.path.join(tmp, "work")
    session_artifact.receive_status(artifact, tmp)
    try:
        session_artifact.receive_tree(artifact, work)
    except (ValueError, OSError, tarfile.TarError) as error:
        print("Session output refused: %s" % error)
        shutil.rmtree(work, ignore_errors=True)
    os.makedirs(os.path.join(tmp, "trusted"), exist_ok=True)
    meta = json.loads(raw)
    meta["work"] = os.path.abspath(work)
    with open(os.path.join(tmp, "trusted", "executor-baseline.json"), "w", encoding="utf-8") as fh:
        json.dump(meta, fh)
    session_artifact.receive_commits(artifact, ".", n)
    return work


def proposals(work, k, source=None):
    text = c.safe_read(work, ".session/requests.json")
    if text:
        requests.process_proposals(text, k, source=source)


def after_session(n, i, labels, role, k, work, status, upd, prose, merged_pending):
    """What a finished session means for the iteration; then close it unless it waits for the owner, a verifier or the
    next iteration."""
    if "loop:shaper" in labels and status == "done" and not merged_pending:
        doc, err = None, None
        try:
            doc = json.loads(c.safe_read(work, ".session/tasks.json") or "")
        except ValueError:
            err = "`.session/tasks.json` is missing or not JSON"
        try:
            got = it.instantiate(k, doc) if doc is not None else err
        except it.PolicyScriptError as e:
            it.fail_iteration(k, "invalid policy script output: %s" % e, rollback=True)
            got = "invalid policy script output: %s" % e
        if isinstance(got, str):
            status, prose = "partial", got
    if role == c.cfg()["verifier_role"] and merged_pending is None:
        status, prose = merge.settle_verification(n, i, status, c.report_fields(n).get("result"), prose)
    if merged_pending:
        return watchdog.reconcile()
    closing.close_out(n, i, status, upd, prose, work=work)
    watchdog.reconcile()
