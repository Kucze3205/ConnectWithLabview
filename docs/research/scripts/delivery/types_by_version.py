"""Group RSRC resource types, LVSR flag sizes and header fields by saved version.

Usage: python3 -I docs/research/scripts/delivery/types_by_version.py [environment_root]

Reads only the prepared read-only cache (default $LABVIEW_ENVIRONMENT).
Uses the prepared pylavi tree; no downloads. Output is JSON on stdout.
"""

import collections
import json
import os
import sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else os.environ.get(
    "LABVIEW_ENVIRONMENT", "/resources/environment"
)
sys.path.insert(0, os.path.join(ROOT, "pylavi"))

from pylavi.file import Resources  # noqa: E402
from pylavi.resource_types import Typevers, TypeLVSR  # noqa: E402

AF = os.path.join(ROOT, "actor-framework")


def major_minor(version) -> str:
    """Collapse a Version to 'major.minor' for grouping"""
    return f"{version.major()}.{version.minor()}"


def main():
    files_by_version = collections.Counter()
    types_by_version = collections.defaultdict(collections.Counter)
    lvsr_sizes = collections.defaultdict(collections.Counter)
    lvsr_version_matches_vers = collections.Counter()
    examples = {}

    for directory, _, names in os.walk(AF):
        if "/.git" in directory:
            continue
        for name in sorted(names):
            path = os.path.join(directory, name)
            with open(path, "rb") as handle:
                if handle.read(4) != b"RSRC":
                    continue
            res = Resources.load(path)
            if "vers" not in res.types():
                continue
            vers = Typevers().from_bytes(res.get_resources("vers")[0][2])
            group = major_minor(vers.version)
            files_by_version[group] += 1
            examples.setdefault(group, os.path.relpath(path, ROOT))
            for rtype in res.types():
                types_by_version[group][rtype] += 1
            if "LVSR" in res.types():
                lvsr = TypeLVSR().from_bytes(res.get_resources("LVSR")[0][2])
                lvsr_sizes[group][lvsr.flags.size()] += 1
                lvsr_version_matches_vers[
                    lvsr.version.value == vers.version.value
                ] += 1

    all_types = set()
    for counter in types_by_version.values():
        all_types.update(counter)
    groups = sorted(files_by_version)
    only_in = {
        g: sorted(
            t
            for t in types_by_version[g]
            if all(t not in types_by_version[o] for o in groups if o != g)
        )
        for g in groups
    }

    print(json.dumps({
        "files_by_major_minor": dict(files_by_version),
        "example_file_by_major_minor": examples,
        "types_only_in_group": only_in,
        "type_counts_by_group": {g: dict(types_by_version[g]) for g in groups},
        "lvsr_flag_bytes_by_group": {
            g: {str(k): v for k, v in lvsr_sizes[g].items()} for g in groups
        },
        "lvsr_version_equals_vers_version": {
            str(k): v for k, v in lvsr_version_matches_vers.items()
        },
    }, indent=1, sort_keys=True))


if __name__ == "__main__":
    main()
