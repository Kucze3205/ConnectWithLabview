#!/usr/bin/env python3
"""Offline inventory of LabVIEW artifact families, save versions and pylavi decoding.

Reads only the prepared public sources under $LABVIEW_ENVIRONMENT
(default /resources/environment). Writes nothing; prints JSON to stdout.

    python3 -I docs/research/scripts/coverage/inventory.py           # JSON inventory
    python3 -I docs/research/scripts/coverage/inventory.py --table   # Markdown tables

Facts are split by origin:
  * "header"/"rsrc": read by this script from the original bytes (own minimal
    RSRC map walker, layout as in @environment/pylavi/pylavi/file.py);
  * "pylavi": result of running the pinned pylavi on the same bytes.
"""

import collections
import hashlib
import io
import json
import os
import re
import struct
import sys
import zipfile
import zlib

sys.dont_write_bytecode = True

ENV = os.environ.get("LABVIEW_ENVIRONMENT", "/resources/environment")
FIXTURE = "Core/ActorFramework/Actor/Actor Core.vi"

FAMILIES = {
    ".vi": "VI",
    ".vit": "VI template",
    ".vim": "malleable VI",
    ".ctl": "control / typedef",
    ".ctt": "control template",
    ".llb": "VI library (LLB)",
    ".mnu": "run-time menu",
    ".rtm": "run-time menu",
    ".xctl": "XControl",
    ".lvlibp": "packed project library",
    ".lvproj": "project (XML)",
    ".lvclass": "class (XML)",
    ".lvlib": "project library (XML)",
    ".lvlps": "project local settings",
    ".aliases": "project aliases",
    ".vipb": "VIPM build spec",
    ".vip": "VI package (zip)",
    ".vipc": "VIPM configuration (zip)",
}
ZIP_EXTS = {".zip", ".vip", ".vipc", ".vsix", ".docx"}
RSRC_MAGIC = b"RSRC\r\n"
XML_VERSION = re.compile(rb'LVVersion="([0-9A-Fa-f]{8})"')
VIPB_VERSION = re.compile(rb"<Package_LabVIEW_Version>([^<]*)<")
SPEC_VERSION = re.compile(rb'LabVIEW Version\s*=\s*"?([^"\r\n]*)')
PHASES = "?dabf"


def decode_version(value):
    """Decode a packed LabVIEW version word (bit layout of pylavi Version)."""
    major = (value >> 28 & 0xF) * 10 + (value >> 24 & 0xF)
    minor, patch, phase = value >> 20 & 0xF, value >> 16 & 0xF, value >> 13 & 0x7
    build = (
        1000 * (value >> 12 & 1)
        + 100 * (value >> 8 & 0xF)
        + 10 * (value >> 4 & 0xF)
        + (value & 0xF)
    )
    text = f"{major}.{minor}.{patch}"
    if phase != 4 or build:
        text += (PHASES[phase] if 1 <= phase <= 4 else f"{{{phase}}}") + str(build)
    return text


def parse_rsrc(data):
    """Walk the RSRC resource map; returns header fields and (type, id, name, payload)."""
    fmt = struct.unpack_from(">H", data, 6)[0]
    ftype, creator = data[8:12], data[12:16]
    moff, msize, doff, dsize = struct.unpack_from(">4I", data, 16)
    names_off = struct.unpack_from(">I", data, moff + 32 + 16)[0]
    base = moff + 32 + 20
    ntypes = struct.unpack_from(">I", data, base)[0] + 1
    resources = []
    for i in range(ntypes):
        code, count, list_off = struct.unpack_from(">4sII", data, base + 4 + 12 * i)
        for j in range(count + 1):
            rid, noff, _, dof, _ = struct.unpack_from(">5I", data, base + list_off + 20 * j)
            size = struct.unpack_from(">I", data, doff + dof)[0]
            payload = data[doff + dof + 4 : doff + dof + 4 + size]
            name = None
            if noff != 0xFFFFFFFF:
                p = moff + names_off + noff
                name = data[p + 1 : p + 1 + data[p]].decode("latin-1")
            resources.append((code.decode("latin-1"), rid, name, payload))
    return {
        "format_version": fmt,
        "file_type": ftype.decode("latin-1"),
        "creator": creator.decode("latin-1"),
        "resources": resources,
    }


def load_pylavi():
    sys.path.insert(0, os.path.join(ENV, "pylavi"))
    from pylavi import resource_types  # pylint: disable=import-outside-toplevel
    from pylavi.file import Resources  # pylint: disable=import-outside-toplevel

    decoders = {
        name[4:]: cls
        for name, cls in sorted(vars(resource_types).items())
        if name.startswith("Type") and isinstance(cls, type)
    }
    return decoders, Resources


DECODERS, PYLAVI_RESOURCES = load_pylavi()


def short_error(exc):
    return f"{type(exc).__name__}: {str(exc)[:60]}"


def pylavi_decode(code, payload):
    """Try the pylavi Type<code> class on one resource payload."""
    cls = DECODERS.get(code.rstrip())
    if cls is None:
        return "opaque"
    try:
        obj = cls().from_bytes(payload)
    except Exception as exc:  # pylint: disable=broad-except
        return "error " + short_error(exc)
    try:
        same = obj.to_bytes() == payload
    except Exception:  # pylint: disable=broad-except
        same = False
    return "decoded" if same else "decoded (no byte round-trip)"


def heap_inflates(payload):
    """True if payload is <u32 size><zlib stream> inflating to that size."""
    if len(payload) < 6:
        return False
    try:
        out = zlib.decompress(payload[4:])
    except zlib.error:
        return False
    return len(out) == struct.unpack_from(">I", payload)[0]


def inspect_rsrc(data, path):
    info = {"kind": "rsrc"}
    try:
        rsrc = parse_rsrc(data)
    except Exception as exc:  # pylint: disable=broad-except
        info["rsrc_error"] = short_error(exc)
        return info
    info.update({k: rsrc[k] for k in ("format_version", "file_type", "creator")})
    by_type = collections.OrderedDict()
    for code, rid, _, payload in rsrc["resources"]:
        by_type.setdefault(code, []).append((rid, payload))
    lvsr = by_type.get("LVSR")
    vers = sorted(by_type.get("vers", []))
    if lvsr and len(lvsr[0][1]) >= 4:
        info["version"] = decode_version(struct.unpack_from(">I", lvsr[0][1])[0])
        info["version_source"] = "LVSR"
    elif vers and len(vers[0][1]) >= 4:
        info["version"] = decode_version(struct.unpack_from(">I", vers[0][1])[0])
        info["version_source"] = f"vers id {vers[0][0]}"
    info["vers"] = sorted(
        {decode_version(struct.unpack_from(">I", p)[0]) for _, p in vers if len(p) >= 4}
    )
    types = {}
    for code, items in by_type.items():
        statuses = collections.Counter(pylavi_decode(code, p) for _, p in items)
        entry = {"count": len(items), "pylavi": dict(statuses)}
        if code.endswith("Hb"):
            entry["zlib_heap"] = sum(heap_inflates(p) for _, p in items)
        types[code] = entry
    info["resource_types"] = types
    if path is None:
        info["pylavi_load"] = "not attempted (archive member)"
    else:
        try:
            loaded = PYLAVI_RESOURCES.load(path)
            same = loaded.types() == list(by_type)
            info["pylavi_load"] = "ok" if same else "ok (type list differs)"
        except Exception as exc:  # pylint: disable=broad-except
            info["pylavi_load"] = "error " + short_error(exc)
    return info


def inspect_bytes(name, data, path, depth):
    ext = os.path.splitext(name)[1].lower()
    if data[:6] == RSRC_MAGIC:
        info = inspect_rsrc(data, path)
    elif ext in ZIP_EXTS and zipfile.is_zipfile(io.BytesIO(data)):
        info = {"kind": "zip", "members": []}
        if depth < 2:
            with zipfile.ZipFile(io.BytesIO(data)) as archive:
                for member in sorted(archive.namelist()):
                    body = archive.read(member)
                    match = SPEC_VERSION.search(body) if member.endswith("spec") else None
                    if match:
                        info["spec_labview_version"] = match.group(1).decode("latin-1").strip()
                    sub = inspect_bytes(member, body, None, depth + 1)
                    if sub is not None:
                        sub["name"] = member
                        info["members"].append(sub)
    elif ext in FAMILIES:
        info = {"kind": "text"}
        match = XML_VERSION.search(data) or VIPB_VERSION.search(data)
        if match and len(match.group(1)) == 8 and match.re is XML_VERSION:
            info["version"] = decode_version(int(match.group(1), 16))
            info["version_source"] = "LVVersion attribute"
        elif match:
            info["version"] = match.group(1).decode("latin-1").strip()
            info["version_source"] = "Package_LabVIEW_Version"
    else:
        return None
    info["family"] = ext if ext in FAMILIES or info["kind"] != "zip" else ext
    return info


def walk():
    for root, dirs, files in os.walk(ENV):
        dirs[:] = sorted(d for d in dirs if d != ".git")
        for name in sorted(files):
            yield os.path.join(root, name)


def summarize(records):
    families = {}
    for rel, info in records:
        fam = families.setdefault(
            info["family"],
            {
                "description": FAMILIES.get(info["family"], "other file with RSRC header"),
                "count": 0,
                "versions": collections.Counter(),
                "version_sources": collections.Counter(),
                "file_types": collections.Counter(),
                "pylavi_load": collections.Counter(),
                "resource_types": {},
                "sample": rel,
            },
        )
        fam["count"] += 1
        fam["versions"][info.get("version", "unknown")] += 1
        fam["version_sources"][info.get("version_source", "none")] += 1
        if "file_type" in info:
            fam["file_types"][info["file_type"]] += 1
        if "pylavi_load" in info:
            fam["pylavi_load"][info["pylavi_load"]] += 1
        for code, entry in info.get("resource_types", {}).items():
            agg = fam["resource_types"].setdefault(code, collections.Counter())
            agg["files"] += 1
            for status, n in entry["pylavi"].items():
                agg[status] += n
    for fam in families.values():
        for key in ("versions", "version_sources", "file_types", "pylavi_load"):
            fam[key] = dict(sorted(fam[key].items()))
        fam["resource_types"] = {k: dict(v) for k, v in sorted(fam["resource_types"].items())}
    return dict(sorted(families.items()))


def inventory():
    top, archived, samples = [], [], {}
    fixture = None
    for path in walk():
        rel = os.path.relpath(path, ENV)
        with open(path, "rb") as handle:
            head = handle.read(6)
        ext = os.path.splitext(path)[1].lower()
        if head != RSRC_MAGIC and ext not in FAMILIES and ext not in ZIP_EXTS:
            continue
        with open(path, "rb") as handle:
            data = handle.read()
        info = inspect_bytes(path, data, path, 0)
        if info is None:
            continue
        if info["kind"] == "zip":
            for member in info["members"]:
                archived.append((f"{rel}!{member['name']}", member))
            if ext not in FAMILIES:
                continue
        top.append((rel, info))
        samples.setdefault(info["family"], (rel, info))
        if rel.endswith(FIXTURE):
            fixture = (rel, info, hashlib.sha256(data).hexdigest())
    result = {
        "environment": ENV,
        "pylavi_decoders": sorted(DECODERS),
        "families": summarize(top),
        "families_in_archives": summarize(archived),
        "samples": {fam: {"path": rel, **info} for fam, (rel, info) in sorted(samples.items())},
    }
    for rel, info in archived:
        samples.setdefault("archive:" + info["family"], (rel, info))
    result["archive_samples"] = {
        fam: {"path": rel, **info}
        for fam, (rel, info) in sorted(samples.items())
        if fam.startswith("archive:")
    }
    if fixture:
        result["fixture"] = {"path": fixture[0], "sha256": fixture[2], **fixture[1]}
    return result


def table(result):
    lines = []
    for key in ("families", "families_in_archives"):
        fams = result[key]
        versions = sorted({v for f in fams.values() for v in f["versions"]})
        lines.append(f"### {key}\n")
        lines.append("| family | files | " + " | ".join(versions) + " |")
        lines.append("|---|---:|" + "---:|" * len(versions))
        for ext, fam in fams.items():
            cells = [str(fam["versions"].get(v, "")) for v in versions]
            lines.append(f"| `{ext}` {fam['description']} | {fam['count']} | " + " | ".join(cells) + " |")
        lines.append("")
    return "\n".join(lines)


def main():
    result = inventory()
    if "--table" in sys.argv[1:]:
        print(table(result))
    else:
        print(json.dumps(result, indent=1, sort_keys=False))


if __name__ == "__main__":
    main()
