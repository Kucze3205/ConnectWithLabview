"""Check XML-derived key files against the artifact and/or the case inventory.

usage: check_xml_keys.py KEY [KEY ...] [--artifact PATH] [--inventory FIXTURE]
Standard library only. Exit 0 on full agreement, 1 otherwise.
"""
import argparse
import hashlib
import json
import re
import sys
import xml.etree.ElementTree as ET

STEP = re.compile(r"^([A-Za-z_][\w.-]*)(?:\[(\d+)\])?$")


def load_claims(path):
    """Return (artifact_sha256, [(claim_id, value, locator)]) for either key shape."""
    with open(path, encoding="utf-8") as f:
        key = json.load(f)
    raw = key["claims"]
    items = []
    if isinstance(raw, dict):
        for cid, c in raw.items():
            items.append((cid, c["value"], c["locator"]))
    else:
        for c in raw:
            items.append((c["claim_id"], c["value"], c["locator"]))
    out = []
    for cid, value, loc in items:
        loc = re.sub(r"\s*\(line \d+\)\s*$", "", loc).strip()
        out.append((cid, value, loc))
    return key.get("artifact_sha256"), out


def resolve(root, locator):
    """Evaluate /Root/Child[n]/.../(@Attr|text()) against a parsed tree."""
    parts = locator.strip("/").split("/")
    if not parts or parts[0] != root.tag:
        raise ValueError("root mismatch")
    node = root
    for part in parts[1:-1]:
        m = STEP.match(part)
        if not m:
            raise ValueError("bad step " + part)
        tag, idx = m.group(1), int(m.group(2) or 1)
        kids = [k for k in node if k.tag == tag]
        if idx < 1 or idx > len(kids):
            raise ValueError("no element " + part)
        node = kids[idx - 1]
    last = parts[-1] if len(parts) > 1 else None
    if last is None:
        raise ValueError("locator has no leaf")
    if last.startswith("@"):
        name = last[1:]
        if name not in node.attrib:
            raise ValueError("no attribute " + name)
        return node.attrib[name]
    if last == "text()":
        return node.text
    raise ValueError("unsupported leaf " + last)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("keys", nargs="+")
    ap.add_argument("--artifact")
    ap.add_argument("--inventory")
    args = ap.parse_args()
    if not args.artifact and not args.inventory:
        ap.error("give --artifact and/or --inventory")

    root = None
    digest = None
    if args.artifact:
        with open(args.artifact, "rb") as f:
            data = f.read()
        digest = hashlib.sha256(data).hexdigest()
        root = ET.fromstring(data)
    inv = {}
    if args.inventory:
        with open(args.inventory, encoding="utf-8") as f:
            for e in json.load(f)["reference_inventory"]:
                cits = e.get("citations") or []
                if cits:
                    inv[e["claim_id"]] = (e["atomic_fact"].get("value"),
                                          cits[0]["locator"]["expression"])

    bad = []
    total = 0
    for kp in args.keys:
        sha, claims = load_claims(kp)
        if root is not None and sha != digest:
            bad.append(f"{kp}: artifact_sha256 key={sha} actual={digest}")
        for cid, value, loc in claims:
            total += 1
            if root is not None:
                try:
                    got = resolve(root, loc)
                except ValueError as exc:
                    got = f"<error: {exc}>"
                if got != value:
                    bad.append(f"{kp}: {cid} artifact mismatch at {loc}: key={value!r} artifact={got!r}")
            if args.inventory:
                if cid not in inv:
                    bad.append(f"{kp}: {cid} not in inventory (or no citation)")
                else:
                    iv, il = inv[cid]
                    if iv != value:
                        bad.append(f"{kp}: {cid} value mismatch: key={value!r} inventory={iv!r} locator={loc}")
                    if il != loc:
                        bad.append(f"{kp}: {cid} locator mismatch: key={loc!r} inventory={il!r}")
    if bad:
        for b in bad:
            print("MISMATCH " + b)
        print(f"xml keys: {total - len({b.split(': ')[1].split(' ')[0] for b in bad if ': A' in b})}/{total} OK")
        return 1
    print(f"xml keys: {total}/{total} OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
