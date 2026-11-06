"""Construiește data/catalog.json din datele vechi (search-data.json) — rulare unică la migrare."""
import json,re,sys,collections
sys.path.insert(0,'tools'); from classify import classify
r=json.load(open('data/legacy-search-data.json'))['records']
out=[];st=collections.Counter();dis=[]
for x in r:
    refs=[f for f in x['refs'] if re.sub(r'[^A-Za-z0-9]','',f)]
    if not refs: st['eliminat-fara-cod']+=1; continue
    g,src=classify(x['en'],refs)
    old=x['group']
    if x.get('categoryVerified') and old!='alte': g,src=old,'verificat'
    elif g is None: g,src=(old,'vechi') if old!='alte' else ('alte','neclasificat')
    elif old!='alte' and g!=old: dis.append((old,g,x['en'],refs[0]))
    st[src]+=1
    out.append({'id':x['id'],'ro':x['ro'],'en':x['en'],'refs':refs,'models':x['models'],'type':x['type'],'group':g,'groupSource':src})
json.dump({'records':out},open('data/catalog.json','w'),ensure_ascii=False,indent=0)
print(st); print('grup final',collections.Counter(x['group'] for x in out))
print('dezacord cu eticheta veche neverificata',len(dis))
import random;random.seed(5)
for d in random.sample(dis,40): print('  ',d)
