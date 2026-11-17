"""The engine's git identity. It authors and commits as the Actions bot, or as the person `engine.yml` names as author
(owner decision of 6 Nov 2026: only the owner's account shows on this loop's commits), set on every git call that writes
history: nothing depends on a global git config of the machine."""
BOT = ("github-actions[bot]", "41898282+github-actions[bot]@users.noreply.github.com")
WRITES_HISTORY = {"commit", "rebase", "merge", "cherry-pick", "revert"}


def env(args, author):
    """The environment for `git <args>`; `author()` returns `engine.yml`'s author and is read only for a call that
    writes history."""
    sub = next((a for i, a in enumerate(args) if a[:1] != "-" and (i == 0 or args[i - 1] != "-c")), "")
    if sub not in WRITES_HISTORY:
        return {}
    a = author()
    name, email = (a["name"], a["email"]) if a.get("name") and a.get("email") else BOT
    return {"GIT_COMMITTER_NAME": name, "GIT_COMMITTER_EMAIL": email, "GIT_AUTHOR_NAME": name, "GIT_AUTHOR_EMAIL": email}
