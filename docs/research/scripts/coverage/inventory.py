"""Inventory LabVIEW artifact families, save versions and pylavi decoding.

Reads only the prepared public sources under $LABVIEW_ENVIRONMENT, offline.
Prints a JSON inventory to stdout; with --table prints Markdown tables instead.

Usage: python3 -I docs/research/scripts/coverage/inventory.py [--table]
"""

import collections
import io
import json
import os
import re
import struct
import sys
import zipfile

ROOT = os.environ.get("LABVIEW_ENVIRONMENT", "/resources/environment")
FIXTURE = "actor-framework/Core/ActorFramework/Actor/Actor Core.vi"
# Extensions LabVIEW or its tooling (VIPM, LabVIEW projects) writes.
LV_EXTS = {
    ".vi", ".vit", ".vim", ".ctl", ".ctt", ".llb", ".mnu", ".rtm", ".uir",
    ".lvclass", ".lvlib", ".lvlibp", ".lvproj", ".lvlps", ".lvsc", ".xctl",
    ".lvtest", ".viancfg", ".vipb", ".vip", ".vipc", ".aliases", ".gbl",
}
ZIP_EXTS = {".zip", ".vip", ".vipc", ".vsix", ".lvlibp"}
XML_VERSION = re.compile(rb'LVVersion="(\d+)"')
STAGES = {0x20: "d", 0x40: "a", 0x60: "b", 0x80: "f"}


def bcd(byte):
    return (byte >> 4) * 10 + (byte & 0x0F)


def version_text(raw):
    """Render a 4-byte LabVIEW version (e.g. 0x20008000) as major.minor.fix stage."""
    if len(raw) < 4:
        return None
    major, minor, fix = bcd(raw[0]), raw[1] >> 4, raw[1] & 0x0F
    stage = STAGES.get(raw[2], f"?{raw[2]:02x}")
    return f"{major}.{minor}.{fix}{stage}{bcd(raw[3])} ({raw[:4].hex()})"


def parse_rsrc(data):
    """Parse a RSRC container without pylavi; return header fields and resources."""
    magic, check, fmt, ftype, creator, md_off, md_size, d_off, d_size = struct.unpack_from(
        ">4s2sH4s4sIIII", data, 0
    )
    if magic != b"RSRC":
        return None
    list_base = md_off + 32 + 20
    names_off = struct.unpack_from(">I", data, md_off + 32 + 16)[0]
    count = struct.unpack_from(">I", data, list_base)[0] + 1
    resources = []
    for i in range(count):
        code, n, list_off = struct.unpack_from(">4sII", data, list_base + 4 + 12 * i)
        for j in range(n + 1):
            rid, name_off, _, r_off, _ = struct.unpack_from(">IIIII", data, list_base + list_off + 20 * j)
            size = struct.unpack_from(">I", data, d_off + r_off)[0]
            name = None
            if name_off != 0xFFFFFFFF:
                p = md_off + names_off + name_off
                name = data[p + 1 : p + 1 + data[p]].decode("latin-1")
            body = data[d_off + r_off + 4 : d_off + r_off + 4 + size]
            resources.append((code.decode("latin-1"), rid, name, body))
    return {
        "format_version": fmt,
        "file_type": ftype.decode("latin-1"),
        "creator": creator.decode("latin-1"),
        "resources": resources,
    }


def rsrc_version(info):
    """Save version from the 'vers' resource (lowest id), cross-checked with LVSR."""
    vers = sorted((rid, body) for code, rid, _, body in info["resources"] if code == "vers")
    lvsr = [body for code, _, _, body in info["resources"] if code == "LVSR"]
    return {
        "vers": version_text(vers[0][1]) if vers else None,
        "vers_ids": [rid for rid, _ in vers],
        "lvsr": version_text(lvsr[0]) if lvsr else None,
    }


def load_pylavi():
    sys.path.insert(0, os.path.join(ROOT, "pylavi"))
    try:
        from pylavi import file as pl_file, resource_types as pl_types
    except Exception as error:  # pylavi missing is reported, not hidden
        return None, None, repr(error)
    return pl_file, pl_types, None


def pylavi_decode(pl_types, code, body):
    """Return (decoder name, status) for one resource body.

    pylavi has no type registry; its classes follow the name Type<fourcc>
    (pylavi/resource_types.py), so lookup is by that name.
    """
    cls = getattr(pl_types, "Type" + code.strip(), None) if pl_types else None
    if cls is None:
        return None, "opaque"
    try:
        value = cls().from_bytes(body)
    except Exception as error:
        return cls.__name__, f"error: {type(error).__name__}"
    try:
        same = value.to_bytes() == body
    except Exception:
        same = False
    return cls.__name__, "decoded" if same else "decoded-not-roundtrip"


def resource_report(pl_types, info):
    per_type = collections.OrderedDict()
    for code, _, _, body in info["resources"]:
        decoder, status = pylavi_decode(pl_types, code, body)
        entry = per_type.setdefault(code, {"count": 0, "decoder": decoder, "status": collections.Counter()})
        entry["count"] += 1
        entry["status"][status] += 1
    return {k: {**v, "status": dict(v["status"])} for k, v in per_type.items()}


def classify(rel, data, pl_file, pl_types):
    """Return (family, version or None, details) for one LabVIEW-related file."""
    ext = os.path.splitext(rel)[1].lower()
    details = {}
    if data[:4] == b"RSRC":
        try:
            info = parse_rsrc(data)
        except struct.error as error:
            return f"{ext} RSRC", None, {"parse_error": repr(error)}
        ver = rsrc_version(info)
        details.update(ver, file_type=info["file_type"], creator=info["creator"])
        details["resource_types"] = [c for c in dict.fromkeys(r[0] for r in info["resources"])]
        if pl_file:
            try:
                pl_file.Resources.load(os.path.join(ROOT, rel))
                details["pylavi_load"] = "ok"
            except Exception as error:
                details["pylavi_load"] = f"error: {type(error).__name__}: {error}"[:200]
        details["_info"] = info
        return f"{ext} RSRC {info['file_type']}", ver["vers"], details
    if data[:4] == b"PK\x03\x04":
        return f"{ext} zip", None, details
    match = XML_VERSION.search(data[:65536])
    if match:
        hexv = match.group(1).decode()
        raw = bytes.fromhex(hexv) if len(hexv) == 8 else b""
        return f"{ext} XML", version_text(raw) or hexv, details
    return f"{ext} text/other", None, details


def walk():
    for directory, dirs, files in os.walk(ROOT):
        dirs[:] = sorted(d for d in dirs if d not in (".git", "node_modules"))
        for name in sorted(files):
            path = os.path.join(directory, name)
            yield os.path.relpath(path, ROOT), path


def inventory():
    pl_file, pl_types, pl_error = load_pylavi()
    families = collections.OrderedDict()
    examples = {}
    all_ext = collections.Counter()

    def add(rel, data, nested_in=None):
        ext = os.path.splitext(rel)[1].lower()
        if ext not in LV_EXTS and data[:4] != b"RSRC":
            return
        family, version, details = classify(rel, data, pl_file if nested_in is None else None, pl_types)
        if nested_in:  # zip members are counted apart: pylavi.Resources.load needs a path on disk
            family += " (zip member)"
            details["magic"] = data[:8].hex()
        elif family.endswith("text/other"):
            details["magic"] = data[:8].hex()
        fam = families.setdefault(family, {
            "count": 0, "versions": collections.Counter(), "sources": collections.Counter(),
            "pylavi_load": collections.Counter(), "resource_types": collections.Counter(),
            "pylavi_types": {},
        })
        fam["count"] += 1
        fam["versions"][version or "no version in header"] += 1
        fam["sources"]["nested in " + os.path.splitext(nested_in)[1] if nested_in else rel.split("/")[0]] += 1
        if "pylavi_load" in details:
            fam["pylavi_load"]["ok" if details["pylavi_load"] == "ok" else "error"] += 1
        info = details.pop("_info", None)
        if info:
            fam["resource_types"].update(details["resource_types"])
            for code, entry in resource_report(pl_types, info).items():
                agg = fam["pylavi_types"].setdefault(code, {"decoder": entry["decoder"], "status": collections.Counter()})
                agg["status"].update(entry["status"])
            if version and details["lvsr"] and details["lvsr"] != version:
                fam.setdefault("vers_lvsr_mismatch", []).append(rel)
        if family not in examples or rel == FIXTURE:
            example = {"path": (nested_in + "!" if nested_in else "") + rel, "version": version, **details}
            if info:
                example["pylavi"] = resource_report(pl_types, info)
            examples[family] = example

    for rel, path in walk():
        ext = os.path.splitext(rel)[1].lower()
        all_ext[ext or "(none)"] += 1
        with open(path, "rb") as handle:
            data = handle.read()
        add(rel, data)
        if ext in ZIP_EXTS and data[:4] == b"PK\x03\x04":
            with zipfile.ZipFile(io.BytesIO(data)) as archive:
                for member in archive.namelist():
                    if os.path.splitext(member)[1].lower() in LV_EXTS:
                        add(member, archive.read(member), nested_in=rel)

    def plain(fam):
        out = dict(fam)
        for key in ("versions", "sources", "pylavi_load", "resource_types"):
            out[key] = dict(sorted(fam[key].items()))
        out["pylavi_types"] = {k: {"decoder": v["decoder"], "status": dict(v["status"])} for k, v in fam["pylavi_types"].items()}
        return out

    decoders = sorted(n for n in dir(pl_types) if n.startswith("Type")) if pl_types else []
    return {
        "root": ROOT,
        "pylavi_import": pl_error or "ok",
        "pylavi_decoders": decoders,
        "families": {k: plain(v) for k, v in sorted(families.items())},
        "examples": examples,
        "fixture": examples.get(next((f for f, e in examples.items() if e["path"] == FIXTURE), None)),
        "all_extensions": dict(all_ext.most_common()),
    }


def table(result):
    lines = ["| Family | Files | Save versions (count) | pylavi load ok/error |", "|---|---|---|---|"]
    for family, fam in result["families"].items():
        versions = "; ".join(f"{v}: {n}" for v, n in fam["versions"].items())
        load = fam["pylavi_load"]
        load_text = f"{load.get('ok', 0)}/{load.get('error', 0)}" if load else "n/a"
        lines.append(f"| {family} | {fam['count']} | {versions} | {load_text} |")
    lines += ["", "| Family | Resource type | Files containing it | pylavi decoder | Status counts |", "|---|---|---|---|---|"]
    for family, fam in result["families"].items():
        for code, entry in fam["pylavi_types"].items():
            status = "; ".join(f"{s}: {n}" for s, n in sorted(entry["status"].items()))
            lines.append(f"| {family} | `{code}` | {fam['resource_types'][code]} | {entry['decoder'] or '-'} | {status} |")
    return "\n".join(lines)


if __name__ == "__main__":
    RESULT = inventory()
    print(table(RESULT) if "--table" in sys.argv[1:] else json.dumps(RESULT, indent=1, default=str))
