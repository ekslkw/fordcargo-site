"""Elimină sufixele/prefixele de stoc ale furnizorului din coduri (ex. „9C46 3304 CB N” -> „9C46 3304 CB”, „Y 3C46 …” -> „3C46 …”).
Păstrează originalele în refs_orig. Scrie data/redirects-piesa.json (slug vechi -> slug nou). Se poate rula de mai multe ori."""
import json,re,collections
def slug(s): return re.sub(r'[^a-z0-9]','',s.replace('İ','').replace('ı','').lower())
FORD=re.compile(r'[A-Z0-9]{1,4}C46')
cat=json.load(open('data/catalog.json'))
recs=cat['records']
# marcajele furnizorului = tot ce apare după poziția 3 în codurile Ford
markers=collections.Counter()
for x in recs:
    for r in x.get('refs_orig',x['refs']):
        t=r.split()
        if t and t[0]=='Y': t=t[1:]
        if t and FORD.fullmatch(t[0]) and len(t)>=4: markers.update(t[3:])
MARK={m for m,c in markers.items() if not m.isdigit()}
KEEP={'STD','STD1','STD2'}
def clean(r):
    t=r.split()
    if len(t)>1 and t[0]=='Y': t=t[1:]
    if t and FORD.fullmatch(t[0]):
        if len(t)>=4: t=t[:3]
        if len(t)==3 and t[2] in ('FİL','DİP','TNS'): t=t[:2]
    elif len(t)>=2 and t[-1] in MARK and t[-1] not in KEEP and t[-1].isalpha(): t=t[:-1]
    return ' '.join(t)
import os
red=json.load(open('data/redirects-piesa.json')) if os.path.exists('data/redirects-piesa.json') else {}
for x in recs:
    if not x['id'].startswith('s'): x.setdefault('refs_orig',x['refs']); continue
    x.setdefault('refs_orig',x['refs'])
    new=list(dict.fromkeys(clean(r) for r in x['refs_orig']))
    x['refs']=new
    for o in x['refs_orig']:
        so,sn=slug(o),slug(clean(o))
        if so!=sn: red[so]=sn
# o fișă = (coduri, denumire); fișele identice după curățare se contopesc
seen={};out=[]
for x in recs:
    k=(tuple(x['refs']),x['ro'])
    if k in seen:
        keep=seen[k]; keep['refs_orig']=list(dict.fromkeys(keep['refs_orig']+x['refs_orig'])); continue
    seen[k]=x; out.append(x)
cat['records']=out
json.dump(cat,open('data/catalog.json','w'),ensure_ascii=False,indent=0)
json.dump(red,open('data/redirects-piesa.json','w'),separators=(',',':'))
pages=len({slug(r) for x in out for r in x['refs']})
print('fișe',len(recs),'->',len(out),'| pagini piese',pages,'| redirecționări',len(red))
