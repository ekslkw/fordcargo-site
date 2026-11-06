"""Separă denumirea turcească originală (Tuna) de marca/producătorul din coada ei."""
import csv,collections,re
NOT_BRAND={'CONTA','FREN','ÇIKMA','VERİLECEKLER','X','FİL','AKTİF','PLAST','MAY','AR','OG','ENG','KOMPLE','SAG','SAĞ','SOL','ON','ÖN','ARKA','UST','ÜST','ALT'}
def load():
    rows=list(csv.DictReader(open('data/source/V17-canli-katalog.csv',encoding='utf-8-sig')))
    ends=collections.Counter(r['original_tr'].split()[-1] for r in rows if r['original_tr'].strip())
    brands={k for k,v in ends.items() if v>=3 and k not in NOT_BRAND}
    return rows,brands
def split(tr,brands):
    t=tr.split(); brand=''
    if t and t[-1] in brands: brand=t.pop()
    while t and len(t[-1])==1 and t[-1].isalpha() and len(t)>1: t.pop()
    return ' '.join(t).strip(' -:.,'),brand
if __name__=='__main__':
    rows,brands=load()
    base=collections.OrderedDict()
    for r in sorted(rows,key=lambda r:r['original_tr']):
        if not r['original_tr'].strip(): continue
        b,br=split(r['original_tr'],brands)
        if not b: continue
        base.setdefault(b,(r['en'],r['ro']))
    with open('data/translations/tr-source.tsv','w',encoding='utf-8') as f:
        for i,(b,(en,ro)) in enumerate(base.items(),1): f.write(f'{i}\t{b}\t{en}\t{ro}\n')
    print('nume TR unice (fără marcă)',len(base),'| fără nume (doar marcă)',sum(1 for r in rows if r['original_tr'].strip() and not split(r['original_tr'],brands)[0]))
