#!/usr/bin/env python3
"""Research-only RSRC/BDHb inspector; stdlib, no LabVIEW or third-party imports.

Run: python3 -I docs/research/poc/inspect_vi.py path/to/add.vi
Offsets named heap_* include the decompressed heap's leading UInt32.
Grammar: pinned pylabview LVheap.py / LVmisc.py; see source-provenance.json.
This reads structural tags, not executable LabVIEW behavior.
"""
import argparse
import hashlib
import json
from pathlib import Path
import struct
import sys
import zlib

MAX_HEAP = 64 * 1024 * 1024


class ParseError(ValueError):
    pass


def require(ok, message):
    if not ok:
        raise ParseError(message)


def rsrc_resources(raw):
    require(len(raw) >= 32, 'truncated RSRC header')
    sig, check, fmt, kind, creator, meta, meta_size, start, size = struct.unpack_from('>4s2sH4s4sIIII', raw)
    require(sig == b'RSRC' and check == b'\r\n' and fmt == 3, 'requires RSRC format 3')
    require(start == 32 and start + size == meta and meta + meta_size <= len(raw), 'invalid RSRC bounds')
    require(meta_size >= 56 and raw[meta:meta + 32] == raw[:32], 'invalid secondary header')
    base = meta + 52
    count = struct.unpack_from('>I', raw, base)[0] + 1
    require(count <= (meta_size - 56) // 12, 'invalid resource type count')
    resources = []
    for index in range(count):
        name, minus_one, offset = struct.unpack_from('>4sII', raw, base + 4 + index * 12)
        table, entries = base + offset, minus_one + 1
        require(table >= base + 4 + count * 12 and table + entries * 20 <= meta + meta_size, 'invalid resource table')
        for entry in range(entries):
            rid, _, _, relative, _ = struct.unpack_from('>IIIII', raw, table + entry * 20)
            location = start + relative
            require(start <= location and location + 4 <= meta, 'invalid resource offset')
            length = struct.unpack_from('>I', raw, location)[0]
            require(location + 4 + length <= meta, 'truncated resource payload')
            resources.append({'type': name.decode('ascii', 'replace'), 'id': rid,
                              'payload_offset': location + 4, 'payload_length': length})
    return resources


class Cursor:
    def __init__(self, data):
        self.data, self.pos = data, 4

    def take(self, n):
        require(0 <= n <= len(self.data) - self.pos, f'truncated field at heap offset {self.pos}; requested {n}')
        result = self.data[self.pos:self.pos + n]
        self.pos += n
        return result

    def integer(self, n, signed=False):
        return int.from_bytes(self.take(n), 'big', signed=signed)

    def u124(self):
        first = self.integer(1)
        return self.integer({255: 2, 254: 4}[first]) if first in (255, 254) else first

    def s124(self):
        first = self.integer(1, True)
        return self.integer({-128: 2, -127: 4}[first], True) if first in (-128, -127) else first

    def s24(self):
        first = self.integer(2, True)
        return self.integer(4, True) if first == -32768 else first


def parse_heap(heap):
    cursor, entries, stack = Cursor(heap), [], []
    entry_start = 0
    try:
        require(len(heap) >= 4, 'missing heap length')
        declared = int.from_bytes(heap[:4], 'big')
        require(declared == len(heap) - 4, f'heap length {declared} differs from {len(heap) - 4}')
        while cursor.pos < len(heap):
            entry_start = cursor.pos
            header = cursor.integer(2)
            size_spec, has_attrs, scope = header >> 13, bool(header & 0x1000), (header >> 10) & 3
            raw_tag = header & 1023
            tag = cursor.integer(4, True) if raw_tag == 1023 else raw_tag - 31
            require(scope in (0, 1, 2), f'reserved scope {scope}')
            require(size_spec != 5, 'unsupported sizeSpec 5')
            attrs = []
            if has_attrs:
                count = cursor.u124()
                require(count <= (len(heap) - cursor.pos) // 3, 'attribute count exceeds remaining bytes')
                for _ in range(count):
                    attr_start = cursor.pos
                    attr_id = cursor.s124()
                    value_offset = cursor.pos
                    value = cursor.s24()
                    attrs.append({'id': attr_id, 'value': value, 'heap_offset': attr_start,
                                  'value_offset': value_offset, 'end': cursor.pos})
            data_size = cursor.u124() if size_spec == 6 else size_spec if 1 <= size_spec <= 4 else 0
            data_offset = cursor.pos
            content = cursor.take(data_size)
            if scope == 2:
                require(bool(stack), 'close without open')
                require(stack[-1] == tag, f'close tag {tag} differs from open {stack[-1]}')
                stack.pop()
            entry = {'heap_offset': entry_start, 'end': cursor.pos, 'header': header,
                     'scope': ('open', 'leaf', 'close')[scope], 'tag': tag, 'depth': len(stack),
                     'size_spec': size_spec, 'attributes': attrs, 'data_offset': data_offset,
                     'data_length': data_size, 'content_hex': content.hex()}
            if size_spec in (0, 7):
                entry['inline_bool'] = size_spec == 7
            entries.append(entry)
            if scope == 0:
                stack.append(tag)
        require(not stack, f'{len(stack)} unclosed tags at end')
        return {'status': 'complete', 'consumed': cursor.pos, 'entries': entries}
    except ParseError as exc:
        return {'status': 'partial', 'failure_entry_offset': entry_start,
                'failure_cursor_offset': cursor.pos, 'reason': str(exc), 'entries': entries}


def inspect(path):
    raw = Path(path).read_bytes()
    resources = rsrc_resources(raw)
    matches = [r for r in resources if r['type'] == 'BDHb' and r['id'] == 0]
    require(len(matches) == 1, 'expected exactly one BDHb resource id 0')
    resource = matches[0]
    offset = resource['payload_offset']
    payload = raw[offset:offset + resource['payload_length']]
    require(len(payload) >= 6, 'truncated BDHb')
    declared = int.from_bytes(payload[:4], 'big')
    require(4 <= declared <= MAX_HEAP, 'invalid or unsupported BDHb uncompressed size')
    stream = zlib.decompressobj()
    heap = stream.decompress(payload[4:], declared + 1)
    require(stream.eof and not stream.unused_data and not stream.unconsumed_tail, 'incomplete or trailing zlib stream')
    require(len(heap) == declared, 'BDHb decompressed-size mismatch')
    parsed = parse_heap(heap)
    return {'artifact': str(path), 'sha256': hashlib.sha256(raw).hexdigest(),
            'heap_sha256': hashlib.sha256(heap).hexdigest(), 'resource': resource,
            'heap_bytes': len(heap), 'heap_length': int.from_bytes(heap[:4], 'big'), **parsed}


def load_labels():
    path = Path(__file__).with_name('heap-labels.json')
    return json.loads(path.read_text()) if path.exists() else {}


def annotate(result, labels):
    """Resolve names using the nearest parent class, as LVheap.tagIdToEnum does."""
    system = labels.get('SL_SYSTEM_TAGS', {})
    fields = labels.get('OBJ_FIELD_TAGS', {})
    class_maps = labels.get('CLASS_EN_TO_TAG_LIST_MAPPING', {})
    stack = []
    for entry in result['entries']:
        key = str(entry['tag'])
        if entry['scope'] == 'close':
            opened, _ = stack.pop()
            entry['name'] = opened['name']
            continue
        parent_class = stack[-1][1] if stack else None
        contextual = labels.get(class_maps.get(str(parent_class), ''), {})
        entry['name'] = system.get(key, contextual.get(key, fields.get(key, f'tag({key})')))
        if entry['scope'] == 'open':
            own_class = next((a['value'] for a in entry['attributes'] if a['id'] == -2), parent_class)
            stack.append((entry, own_class))


def tree_lines(result, labels):
    classes = labels.get('SL_CLASS_TAGS', {})
    attrs = labels.get('SL_SYSTEM_ATTRIB_TAGS', {})
    lines = []
    for entry in result['entries']:
        tag = entry['tag']
        name = entry.get('name', f'tag({tag})')
        marker = {'open': '+', 'leaf': '=', 'close': '-'}[entry['scope']]
        details = []
        for attr in entry['attributes']:
            value = classes.get(str(attr['value']), str(attr['value'])) if attr['id'] == -2 else str(attr['value'])
            details.append(f"{attrs.get(str(attr['id']), str(attr['id']))}={value}")
        content = bytes.fromhex(entry['content_hex'])
        if content:
            value = str(int.from_bytes(content, 'big')) if len(content) <= 4 else f'{len(content)} bytes'
            details.append(f"data@{entry['data_offset']}={value}")
        elif entry['scope'] == 'leaf':
            details.append(f"no-payload(sizeSpec={entry['size_spec']})")
        lines.append(f"{entry['heap_offset']:04d} {'  ' * entry['depth']}{marker} {name} [{tag}] {' '.join(details)}".rstrip())
    return lines


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('path')
    parser.add_argument('--output', type=Path, help='save complete JSON evidence')
    parser.add_argument('--tree-output', type=Path, help='save full indented tree')
    parser.add_argument('--max-lines', type=int, default=60)
    args = parser.parse_args()
    try:
        result = inspect(args.path)
        labels = load_labels()
        annotate(result, labels)
        lines = tree_lines(result, labels)
        if args.output:
            args.output.write_text(json.dumps(result, indent=2) + '\n')
        if args.tree_output:
            args.tree_output.write_text('\n'.join(lines) + '\n')
        print(f"artifact={result['artifact']} sha256={result['sha256']}")
        print(f"heap_bytes={result['heap_bytes']} entries={len(lines)} parse={result['status']}; offsets include heap UInt32")
        shown = max(0, min(args.max_lines, 70))
        print('\n'.join(lines[:shown]))
        if len(lines) > shown:
            print(f'{len(lines) - shown} tree lines omitted; use --tree-output for all entries')
        if result['status'] != 'complete':
            print(f"PARSE FAILURE entry@{result['failure_entry_offset']} cursor@{result['failure_cursor_offset']}: {result['reason']}")
            return 1
        print(f"COMPLETE consumed={result['consumed']}; scopes balanced, inner/outer lengths and zlib checksum valid")
        return 0
    except (OSError, ValueError, struct.error, zlib.error) as exc:
        print(f'PARSE FAILURE: {exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
