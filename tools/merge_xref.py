"""Corespondențe verificate cod Ford <-> cod T/FINIS (data/xref/verificate.tsv) aplicate pe catalog.
Se rulează după add_finis/clean_codes și înainte de build_catalog. Idempotent.
- dacă ambele coduri sunt în fișe diferite: fișa mai mică se unește în cea mai mare (fiecare cod își păstrează pagina)
- dacă lipsește un cod: se adaugă la fișa existentă
- fișe noi: data/xref/fise-noi.tsv (cod Ford, cod T/FINIS, grupă, denumire RO, denumire EN)
Nu se preiau denumiri, descrieri sau imagini din surse externe; doar corespondența de coduri."""
import json,re
C='data/catalog.json'; R='data/redirects-all.json'
cat=json.load(open(C)); recs=cat['records']; red=json.load(open(R))
N=lambda s:re.sub(r'[^A-Z0-9]','',s.upper())
def slug(s): return re.sub(r'[^a-z0-9]','',s.replace('İ','').replace('ı','').lower())
def find(code): return [r for r in recs if any(N(x)==N(code) for x in r['refs'])]
def fmt(code):
    c=N(code)
    m=re.fullmatch(r'([0-9A-Z]{2}C4[46])([0-9A-Z]+?)([A-Z]{2,}[0-9A-Z]*)',c)
    return f'{m.group(1)} {m.group(2)} {m.group(3)}' if m else code
log=[]
for l in open('data/xref/verificate.tsv',encoding='utf-8'):
    if l.startswith('#') or not l.strip(): continue
    ford,t=l.rstrip('\n').split('\t')[:2]
    A=find(ford); B=find(t)
    if not A and not B: continue
    if A and not B: A[0]['refs'].append(t); log.append(('+T',ford,t)); continue
    if B and not A: B[0]['refs'].append(fmt(ford)); log.append(('+Ford',ford,t)); continue
    a,b=A[0],B[0]
    if a is b: continue
    keep,drop=(a,b) if len(a['refs'])>=len(b['refs']) else (b,a)
    if drop['type']!='finis' and keep['type']=='finis': keep,drop=drop,keep
    old=slug(drop['refs'][0]); new=slug(keep['refs'][0])
    for x in drop['refs']:
        if N(x) not in {N(y) for y in keep['refs']}: keep['refs'].append(x)
    recs.remove(drop)
    log.append(('unit',ford,t,old,'->',new))
for l in open('data/xref/fise-noi.tsv',encoding='utf-8'):
    if l.startswith('#') or not l.strip(): continue
    ford,t,g,ro,en=l.rstrip('\n').split('\t')
    if find(ford) or find(t): continue
    recs.append({'id':'v'+N(ford).lower(),'ro':ro,'en':en,'refs':[ford,t],'models':[],'type':'catalog','group':g,'groupSource':'verificat'})
    log.append(('nou',ford,t))
# denumiri verificate pentru coduri cu denumiri contradictorii: toate fișele codului devin una
for l in open('data/xref/nume-verificate.tsv',encoding='utf-8'):
    if l.startswith('#') or not l.strip(): continue
    ford,t,ro,en=l.rstrip('\n').split('\t')
    A=find(ford)
    if not A: continue
    keep=max(A,key=lambda r:len(r['refs']))
    for d in A:
        if d is keep: continue
        for x in d['refs']:
            if N(x) not in {N(y) for y in keep['refs']}: keep['refs'].append(x)
        recs.remove(d)
    if t and N(t) not in {N(y) for y in keep['refs']}:
        B=[r for r in find(t) if r is not keep]
        for d in B:
            if d['type']=='finis' and len(d['refs'])==1: recs.remove(d)
        keep['refs'].append(t)
    if keep['ro']!=ro: log.append(('nume-verif',ford,keep['ro'],'->',ro))
    keep['ro']=ro; keep['en']=en; keep['groupSource']='verificat'
# denumire greșită: „connecting rod” = bielă, nu bară de legătură
for r in recs:
    if r['group']=='motor' and r['en'].lower().startswith('connecting rod') and re.match(r'(Bară|Tijă) de legătură',r['ro']):
        r['ro']=re.sub(r'^(Bară|Tijă) de legătură','Bielă',r['ro']); log.append(('nume',r['refs'][0],r['ro']))
json.dump(cat,open(C,'w'),ensure_ascii=False)
for x in log: print(*x)
print('fișe',len(recs))
