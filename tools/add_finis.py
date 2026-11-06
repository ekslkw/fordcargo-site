"""Adaugă codurile T/FINIS (data/source/T-FINIS-kaynak-fiyatsiz.csv — FĂRĂ prețuri) în data/catalog.json.
- Cod T cu corespondent Ford cunoscut (data/xref/*) -> se adaugă la fișa Ford existentă (aceeași pagină, „Referințe asociate”).
- Altfel -> fișă nouă (id f…), denumire din data/translations/finis/out-*.tsv.
Se rulează după clean_codes.py; se poate rula de mai multe ori."""
import csv,json,re,glob,collections,sys,os
sys.path.insert(0,os.path.dirname(__file__)); from classify import classify
slug=lambda s:re.sub(r'[^a-z0-9]','',s.replace('İ','').replace('ı','').lower())
norm=lambda s:re.sub(r'\s+',' ',s.strip().upper())
rows=list(csv.DictReader(open('data/source/T-FINIS-kaynak-fiyatsiz.csv',encoding='utf-8-sig')))
assert set(rows[0].keys())=={'excel_row','code','source_name'}, 'sursa nu trebuie să conțină prețuri'
src={}
for l in open('data/translations/finis/source.tsv',encoding='utf-8'):
    i,n,_=l.rstrip('\n').split('\t'); src[n]=i
tr={}
for f in ['data/translations/finis/final.tsv']:
    for l in open(f,encoding='utf-8'):
        p=l.rstrip('\n').split('\t')
        if len(p)==3 and p[1] and p[2]: tr[p[0]]=(p[1].strip(),p[2].strip())
# corespondențe T -> cod Ford
xref=collections.defaultdict(set)
d=json.load(open('data/xref/t-reference-research.json'))
for r in d['records']:
    for t in r.get('t_references',[])+r.get('alternative_t_references',[]):
        for e in r.get('engineering_references',[]): xref[t].add(e)
for xf in sorted(glob.glob('data/xref/*.tsv')):
    for l in open(xf,encoding='utf-8'):
        if l.startswith('#') or '\t' not in l: continue
        t,e=l.rstrip('\n').split('\t')[:2]; xref[t.strip()].add(re.sub(r'-',' ',e.strip()))
cat=json.load(open('data/catalog.json')); recs=[x for x in cat['records'] if x.get('type')!='finis']
for x in recs: x['refs']=[r for r in x['refs'] if not x.get('finis_added') or r not in x['finis_added']]; x.pop('finis_added',None)
byslug={}
for x in recs:
    for r in x['refs']: byslug.setdefault(slug(r),x)
def ford_slug(e):
    e=re.sub(r'^(KIT|ME)','',re.sub(r'[\s\-]','',e.upper()))
    return slug(e)
NONFORD=re.compile(r'\b(OTOKAR|JUMBO|MAN)\b',re.I)  # piese pentru alte mărci de vehicule — nu se publică pe site-ul Ford
st=collections.Counter(); new=[]
for r in rows:
    code=r['code'].strip()
    if not code: continue
    if NONFORD.search(r['source_name']): st['non_ford']+=1; continue
    if slug(code) in byslug: st['deja']+=1; continue
    target=None
    for e in xref.get(code,[]):
        s=ford_slug(e)
        target=byslug.get(s) or next((byslug[k] for k in byslug if k.startswith(s) and len(k)-len(s)<=1),None)
        if target: break
    if target:
        target['refs'].append(code); target.setdefault('finis_added',[]).append(code); byslug[slug(code)]=target; st['legat']+=1; continue
    n=norm(r['source_name']); fid=src.get(n)
    en,ro=tr.get(fid,(None,None)) if fid else (None,None)
    if not en: en,ro=(r['source_name'].strip().capitalize() or 'Ford part', 'Piesă pentru camioane Ford') ; st['fara_traducere']+=1
    extra=[e for e in sorted(xref.get(code,[])) if re.search(r'C4[46]',e) and slug(e) not in byslug]
    g,gs=classify(en,[code]+extra)
    x={'id':'f'+r['excel_row'],'ro':ro,'en':en,'refs':[code]+extra,'models':[],'type':'finis','group':g or 'alte','groupSource':gs or 'neclasificat','en_orig':r['source_name']}
    new.append(x); byslug[slug(code)]=x; st['nou']+=1
    for e in extra: byslug[slug(e)]=x; st['cod_ford_adaugat']+=1
cat['records']=recs+new
json.dump(cat,open('data/catalog.json','w'),ensure_ascii=False,indent=0)
print(dict(st))
