#!/usr/bin/env python3
"""Offline downgrade helper: preserve current split account settings in legacy store.
Stop the only writer first. This only creates a new private output file; it never
changes the live store or removes the split directory. After verification, install
the output atomically and retain/rename account-configs before starting old code.
"""
import argparse,json,os,re
from pathlib import Path
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--data-dir',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
a=p.parse_args();os.umask(0o077);root=a.data_dir
store=json.loads((root/'store.json').read_text());directory=root/'account-configs'
assert isinstance(store,dict) and directory.is_dir() and not directory.is_symlink()
assert json.loads((directory/'.format.json').read_text())=={'version':1},'unsupported split format'
configs={}
for f in directory.iterdir():
 if f.name=='.format.json':continue
 assert f.is_file() and not f.is_symlink(),'unexpected config entry'
 assert f.name.endswith('.json'),'unexpected config filename'
 stem=f.name[:-5]
 if re.fullmatch(r'[0-9]+',stem):ident=stem
 else:
  assert re.fullmatch(r'id-(?:[0-9a-f]{2})+',stem),'invalid encoded account ID'
  ident=bytes.fromhex(stem[3:]).decode('utf-8')
 assert ident and ident==ident.strip()
 expected=ident if re.fullmatch(r'[0-9]+',ident) else 'id-'+ident.encode().hex()
 assert expected+'.json'==f.name and ident not in configs
 value=json.loads(f.read_text());assert isinstance(value,dict);configs[ident]=value
store.pop('accountConfigStorageVersion',None);store['accountConfigs']=configs
encoded=json.dumps(store,ensure_ascii=False,indent=2).encode()+b'\n'
fd=os.open(a.output,os.O_CREAT|os.O_EXCL|os.O_WRONLY|os.O_NOFOLLOW,0o600)
with os.fdopen(fd,'wb') as f:f.write(encoded);f.flush();os.fsync(f.fileno())
assert json.loads(a.output.read_bytes())==store
print(json.dumps({'account_configs':len(configs),'output_bytes':len(encoded),'verified':True}))
