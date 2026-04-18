import re
from pathlib import Path

base = Path(__file__).resolve().parent
changed = []
for path in sorted(base.rglob('tc*.yml')):
    if path.name in ('folder.yml', 'opencollection.yml'):
        continue
    m = re.match(r'tc(\d{3})_', path.name)
    if not m:
        continue
    upper = f'TC{m.group(1)}'
    lower = f'tc{m.group(1)}'
    text = path.read_text(encoding='utf-8')
    orig = text
    text = re.sub(r'^(\s*name:\s*)TC\d{3}', lambda mo: mo.group(1) + upper, text, count=1, flags=re.M)
    info_block = re.search(r'^(info:\n(?:[ \t].*\n)*)', text, flags=re.M)
    if info_block:
        new_info = re.sub(r'^([ \t]*-\s*)tc\d{3}', r'\1' + lower, info_block.group(1), count=1, flags=re.M)
        text = text[:info_block.start(1)] + new_info + text[info_block.end(1):]
    if text != orig:
        path.write_text(text, encoding='utf-8')
        changed.append(str(path.relative_to(base)))

print('updated', len(changed), 'files')
for p in changed:
    print(p)
