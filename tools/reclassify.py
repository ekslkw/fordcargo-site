"""Recalculează grupele fișelor neverificate manual, pe baza denumirii EN actuale."""
import json,sys,os,collections
sys.path.insert(0,os.path.dirname(__file__)); from classify import classify
cat=json.load(open('data/catalog.json')); ch=0
for x in cat['records']:
    if x.get('groupSource')=='verificat': continue
    g,src=classify(x['en'],x['refs'])
    if g and g!=x['group']: x['group']=g; x['groupSource']=src; ch+=1
json.dump(cat,open('data/catalog.json','w'),ensure_ascii=False,indent=0)
print('schimbate',ch,collections.Counter(x['group'] for x in cat['records']))
