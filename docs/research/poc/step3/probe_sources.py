"""Bounded source search; no network and no source imports."""
import ast
import hashlib
import json
import os
from pathlib import Path
import re

BASE = Path(__file__).resolve().parents[1]
ENV = Path(os.environ.get('LABVIEW_ENVIRONMENT', '/resources/environment'))
PATTERNS = {
    'primitive_contract': r'primIndex|primResID|\b(Add|Subtract)\b',
    'integrity_cache': r'BDPW|checksum|password|invalidate|recompil|compiled|VICD|CPC2',
    'constant_encoding': r'OF__typeDesc|OF__data|NODE_DATAFILL|parseRSRCContentDirect|NumInt|NumUInt|NumFloat|Boolean|String',
}

def main():
    result = {'method': 'regex search of complete named snapshots and prepared pylavi Python sources; class inventory via AST; matches are discovery aids, not semantic proof', 'files': []}
    paths = [BASE / n for n in ('LVheap-source.txt', 'LVmisc-source.txt', 'LVparts-source.txt')]
    paths += sorted((ENV / 'pylavi' / 'pylavi').glob('*.py'))
    for path in paths:
        raw = path.read_bytes()
        text = raw.decode()
        local = path.is_relative_to(BASE)
        item = {'path': str(path.relative_to(BASE)) if local else str(path.relative_to(ENV)), 'origin': 'saved' if local else 'prepared', 'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw), 'classes': [n.name for n in ast.parse(text).body if isinstance(n, ast.ClassDef)], 'matches': {}}
        for name, pattern in PATTERNS.items():
            item['matches'][name] = [{'line': i, 'text': s} for i, s in enumerate(text.splitlines(), 1) if re.search(pattern, s, re.I)]
        result['files'].append(item)
    out = BASE / 'step3' / 'source-search.json'
    out.write_text(json.dumps(result, indent=2) + '\n')
    for item in result['files']:
        print(item['path'], item['bytes'], {k: len(v) for k, v in item['matches'].items()})
    print('saved', out.name)

if __name__ == '__main__':
    main()
