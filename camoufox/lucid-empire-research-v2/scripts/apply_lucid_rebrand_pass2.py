#!/usr/bin/env python3
import os, subprocess, re
OLD_NAME='camoufox'
NEW_NAME='lucid_browser'
OLD_TITLE='Camoufox'
NEW_TITLE='Lucid Empire'
root=os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
print('Pass 2: scanning git grep matches...')
matches = subprocess.check_output(['git','grep','-l','camoufox\|Camoufox'], text=True).splitlines()
modified=[]
for fp in matches:
    # skip binary-ish
    if any(fp.endswith(ext) for ext in ['.zip','.png','.db','.ico','.icns','.7z']):
        continue
    try:
        with open(fp,'r',encoding='utf-8',errors='ignore') as f:
            s=f.read()
    except Exception:
        continue
    new = s.replace(OLD_TITLE, NEW_TITLE).replace(OLD_NAME, NEW_NAME)
    if new!=s:
        with open(fp,'w',encoding='utf-8') as f:
            f.write(new)
        modified.append(fp)
        print('[MODIFIED]', fp)
# special: update pythonlib/pyproject.toml name if exists
pyp=os.path.join(root,'pythonlib','pyproject.toml')
if os.path.exists(pyp):
    with open(pyp,'r',encoding='utf-8',errors='ignore') as f:
        s=f.read()
    s2=s.replace('name = "camoufox"','name = "lucid_browser"').replace('Camoufox','Lucid Empire')
    if s2!=s:
        with open(pyp,'w',encoding='utf-8') as f:
            f.write(s2)
        modified.append(pyp)
        print('[MODIFIED]', pyp)

print('\nPass 2 done. modified:', len(modified))
