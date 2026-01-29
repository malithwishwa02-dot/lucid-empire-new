#!/usr/bin/env python3
import os, re, shutil
ROOT=os.path.dirname(os.path.abspath(__file__))+'/..'
ROOT=os.path.abspath(ROOT)
OLD_NAME='lucid_browser'
NEW_NAME='lucid_browser'
OLD_TITLE='Lucid Empire'
NEW_TITLE='Lucid Empire'
EXCLUDES={'LUCID_REBRAND_PROTOCOL.py','.git','node_modules','venv'}
EXTS=('.py','.js','.md','.txt','.json','.yml','.sh','.cpp','.h','.patch','.properties','.xhtml','.cfg')
modified=[]
renamed=[]
report_lines=[]

print('Starting rebrand in:', ROOT)

# Content replacements
for dirpath, dirnames, filenames in os.walk(ROOT):
    # skip excluded dirs entirely
    if any(ex in dirpath.split(os.sep) for ex in EXCLUDES):
        continue
    for fn in filenames:
        if fn in EXCLUDES:
            continue
        fp=os.path.join(dirpath,fn)
        # only consider likely text files by extension
        if not fn.lower().endswith(EXTS):
            continue
        try:
            with open(fp,'r',encoding='utf-8',errors='ignore') as f:
                s=f.read()
        except Exception as e:
            continue
        if OLD_NAME in s or OLD_TITLE in s:
            new = s.replace(OLD_NAME, NEW_NAME)
            new = new.replace(OLD_TITLE, NEW_TITLE)
            # additional obfuscation: remove daijro copyright
            new = re.sub(r'Copyright (c) 2026 Lucid Empire', 'Copyright (c) 2026 Lucid Empire', new, flags=re.IGNORECASE)
            # If changed, write and log
            if new != s:
                with open(fp,'w',encoding='utf-8') as f:
                    f.write(new)
                modified.append(fp)
                report_lines.append(f'MODIFIED: {fp}')
                print('[MODIFIED]', fp)

# Rename filesystem objects bottom-up
for dirpath, dirnames, filenames in os.walk(ROOT, topdown=False):
    if any(ex in dirpath.split(os.sep) for ex in EXCLUDES):
        continue
    # files
    for fn in filenames:
        if OLD_NAME in fn:
            oldp=os.path.join(dirpath,fn)
            newfn=fn.replace(OLD_NAME, NEW_NAME)
            newp=os.path.join(dirpath,newfn)
            if os.path.exists(newp):
                # if collision, create unique name
                base,ext=os.path.splitext(newp)
                newp=base+'_renamed'+ext
            os.rename(oldp,newp)
            renamed.append((oldp,newp))
            report_lines.append(f'RENAMED: {oldp} -> {newp}')
            print('[RENAMED]', oldp, '->', newp)
    # dirs
    for dn in dirnames:
        if OLD_NAME in dn:
            oldp=os.path.join(dirpath,dn)
            newdn=dn.replace(OLD_NAME, NEW_NAME)
            newp=os.path.join(dirpath,newdn)
            if os.path.exists(newp):
                newp=newp+'_renamed'
            os.rename(oldp,newp)
            renamed.append((oldp,newp))
            report_lines.append(f'RENAMED DIR: {oldp} -> {newp}')
            print('[RENAMED DIR]', oldp, '->', newp)

# Metadata purge: move README_LUCID.md to README.md
lucid_readme=os.path.join(ROOT,'README_LUCID.md')
readme=os.path.join(ROOT,'README.md')
if os.path.exists(lucid_readme):
    if os.path.exists(readme):
        os.remove(readme)
    os.rename(lucid_readme, readme)
    report_lines.append('README replaced with README_LUCID.md')
    print('[README] Replaced README.md with README_LUCID.md')

# Update pyproject if exists
pyproj=os.path.join(ROOT,'pythonlib','pyproject.toml')
if os.path.exists(pyproj):
    try:
        with open(pyproj,'r',encoding='utf-8',errors='ignore') as f:
            s=f.read()
        s2=s.replace(OLD_NAME, NEW_NAME).replace(OLD_TITLE, NEW_TITLE)
        if s2!=s:
            with open(pyproj,'w',encoding='utf-8') as f:
                f.write(s2)
            report_lines.append('pyproject.toml updated')
            print('[pyproject] updated')
    except Exception:
        pass

# Write transformation report
report_file=os.path.join(ROOT,'LUCID_TRANSFORMATION_REPORT.md')
with open(report_file,'w',encoding='utf-8') as f:
    f.write('# LUCID REBRAND TRANSFORMATION REPORT\n\n')
    f.write(f'Modified files: {len(modified)}\n')
    f.write(f'Renamed paths: {len(renamed)}\n\n')
    for line in report_lines:
        f.write(line + '\n')

# Write modified files list
modfile=os.path.join(ROOT,'LUCID_MODIFIED_FILES.txt')
with open(modfile,'w',encoding='utf-8') as f:
    for m in modified:
        f.write(m+'\n')

print('\nDone. Summary:')
print(' - files modified:', len(modified))
print(' - files/dirs renamed:', len(renamed))
print(' - report:', report_file)
