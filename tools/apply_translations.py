"""Aplică denumirile RO/EN în data/catalog.json.
Prioritate: 1) traducere din denumirea turcească originală (data/translations/tr-final.tsv, ID T…),
2) corectură pentru fișele fără sursă turcă (ID E…), 3) denumirea originală.
Originalele se păstrează în en_orig/ro_orig. Se poate rula de mai multe ori."""
import json,sys,os
sys.path.insert(0,os.path.dirname(__file__)); from tr_base import load,split
from classify import ford_range,base
rows,brands=load(); trmap={r['id']:r['original_tr'] for r in rows}
T={};E={}
for l in open('data/translations/tr-source.tsv',encoding='utf-8'):
    i,b,_,_=l.rstrip('\n').split('\t'); T[b]='T'+i
for l in open('data/translations/en-source.tsv',encoding='utf-8'):
    i,en,ro=l.rstrip('\n').split('\t'); E[(en,ro)]=i
F={}
# denumiri generice după grupa de numerotare Ford, pentru codurile fără nicio denumire în sursă
GEN={'motor':('Engine component for Ford trucks','Componentă motor pentru camioane Ford'),'transmisie':('Driveline component for Ford trucks','Componentă transmisie pentru camioane Ford'),
 'franare':('Brake system component for Ford trucks','Componentă sistem de frânare pentru camioane Ford'),'suspensie':('Suspension / wheel component for Ford trucks','Componentă suspensie / roată pentru camioane Ford'),
 'directie':('Steering / front axle component for Ford trucks','Componentă direcție / punte față pentru camioane Ford'),'electric':('Electrical component for Ford trucks','Componentă electrică pentru camioane Ford'),
 'racire':('Cooling system component for Ford trucks','Componentă sistem de răcire pentru camioane Ford'),'cabina':('Cab / body component for Ford trucks','Componentă cabină / caroserie pentru camioane Ford'),
 'alimentare':('Fuel / emissions system component for Ford trucks','Componentă sistem de alimentare / emisii pentru camioane Ford'),'climatizare':('Heating / A/C component for Ford trucks','Componentă încălzire / climatizare pentru camioane Ford')}
for l in open('data/translations/tr-final.tsv',encoding='utf-8'):
    i,en,ro=l.rstrip('\n').split('\t'); F[i]=(en,ro)
cat=json.load(open('data/catalog.json')); st={'tr':0,'en':0,'generic':0,'orig':0}
for x in cat['records']:
    if x.get('type')=='finis': continue
    x.setdefault('en_orig',x['en']); x.setdefault('ro_orig',x['ro'])
    tr=trmap.get(x['id'],'').strip(); x['tr_orig']=tr
    if tr:
        b,_=split(tr,brands)
        if b and T.get(b) in F: x['en'],x['ro']=F[T[b]]; st['tr']+=1; continue
        if not b:
            g=next((ford_range(base(r)) for r in x['refs'] if ford_range(base(r))),None)
            x['en'],x['ro']=GEN.get(g,('Part for Ford trucks','Piesă pentru camioane Ford')); st['generic']+=1; continue
    k=E.get((x['en_orig'],x['ro_orig']))
    if k in F: x['en'],x['ro']=F[k]; st['en']+=1
    else: x['en'],x['ro']=x['en_orig'],x['ro_orig']; st['orig']+=1
json.dump(cat,open('data/catalog.json','w'),ensure_ascii=False,indent=0)
print(st)
