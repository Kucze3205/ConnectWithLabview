"""Count artifact families and saved LabVIEW versions in the prepared sources.

Usage: python3 -I docs/research/scripts/delivery/versions.py [environment_root]

Reads only the prepared read-only cache (default $LABVIEW_ENVIRONMENT).
Uses the prepared pylavi tree for RSRC files; no downloads.
"""

import collections
import json
import os
import re
import sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else os.environ.get(
    "LABVIEW_ENVIRONMENT", "/resources/environment"
)
sys.path.insert(0, os.path.join(ROOT, "pylavi"))

from pylavi.file import Resources  # noqa: E402
from pylavi.resource_types import Typevers, TypeLVSR  # noqa: E402

AF = os.path.join(ROOT, "actor-framework")
XML_VERSION = re.compile(rb'LVVersion="(\d+)"')


def main():
    extensions = collections.Counter()
    rsrc_ok = collections.Counter()
    rsrc_fail = collections.Counter()
    failures = []
    versions = collections.Counter()
    xml_versions = collections.Counter()
    types_seen = collections.Counter()
    file_types = collections.Counter()

    for directory, _, names in os.walk(AF):
        if "/.git" in directory:
            continue
        for name in names:
            path = os.path.join(directory, name)
            ext = os.path.splitext(name)[1].lower() or "(none)"
            extensions[ext] += 1
            with open(path, "rb") as handle:
                head = handle.read(4096)
            if head[:4] == b"RSRC":
                try:
                    res = Resources.load(path)
                except (AssertionError, Exception) as error:  # pylint: disable=broad-except
                    rsrc_fail[ext] += 1
                    failures.append((os.path.relpath(path, AF), repr(error)[:160]))
                    continue
                rsrc_ok[ext] += 1
                file_types[res.file_type.to_string()] += 1
                for rtype in res.types():
                    types_seen[rtype] += 1
                if "vers" in res.types():
                    data = res.get_resources("vers")[0][2]
                    try:
                        vers = Typevers().from_bytes(data)
                        versions[vers.version.to_string()] += 1
                    except AssertionError:
                        versions["(vers undecoded)"] += 1
                if "LVSR" in res.types():
                    TypeLVSR().from_bytes(res.get_resources("LVSR")[0][2])
            else:
                match = XML_VERSION.search(head)
                if match:
                    xml_versions[(ext, match.group(1).decode())] += 1

    print(json.dumps({
        "extensions": extensions.most_common(),
        "rsrc_loaded_by_ext": rsrc_ok.most_common(),
        "rsrc_failed_by_ext": rsrc_fail.most_common(),
        "rsrc_failures_sample": failures[:10],
        "rsrc_file_types": file_types.most_common(),
        "vers_versions": versions.most_common(),
        "xml_LVVersion_by_ext": [[list(k), v] for k, v in xml_versions.most_common()],
        "resource_type_file_counts": types_seen.most_common(),
    }, indent=1))


if __name__ == "__main__":
    main()
