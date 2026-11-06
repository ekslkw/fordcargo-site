"""Aplică antetul/subsolul comun și corecturile globale pe paginile statice (cele negenerate). Se poate rula de mai multe ori."""
import os,re,sys,html
sys.path.insert(0,os.path.dirname(__file__)); import layout
D='dist'; GEN=('piesa/','categorie/','referinte/','en/references/')
CAT_LABELS={'Suspensie':'Suspensie și roți','Turbocompresor':'Turbo, admisie și evacuare','Filtre și consumabile':'Filtre și întreținere',
            'Climatizare':'Încălzire și climatizare','Alimentare și injecție':'Alimentare, injecție și AdBlue'}
FORD_TEXT=[('Experiență din 1990.O echipă','Experiență din 1990. O echipă'),('<title>Piese Ford Trucks — Cargo','<title>Piese pentru camioane Ford Trucks — Cargo'),
 ('Catalog piese Ford Trucks','Catalog piese pentru camioane Ford Trucks'),('| Piese Ford Trucks și','| Piese pentru camioane Ford Trucks și'),
 ('Cere ofertă pentru piese Ford Trucks','Cere ofertă pentru piese de camioane Ford Trucks'),('Caută piese Ford Trucks după','Caută piese pentru camioane Ford Trucks după'),
 ('despre piese Ford','despre piese pentru camioane Ford'),('identificarea pieselor Ford','identificarea pieselor pentru camioane Ford'),
 (' | FordCargo</title>',' | EKS LKW</title>'),('content="FordCargo.ro — EKS LKW"','content="EKS LKW — piese pentru camioane Ford"')]
KEEP_OUT={'/site.js','/privacy-controls.js'}
n=0
import json
PMAP=json.load(open('data/redirects-piesa.json'))
for k,v in json.load(open('data/redirects-all.json')).items():
    m1=re.fullmatch(r'/piesa/([a-z0-9]+)/',k); m2=re.fullmatch(r'/piesa/([a-z0-9]+)/',v)
    if m1 and m2: PMAP[m1.group(1)]=m2.group(1)
for k in list(PMAP):
    v=PMAP[k]; n=0
    while v in PMAP and PMAP[v]!=v and n<5: v=PMAP[v]; n+=1
    PMAP[k]=v
for dp,_,fs in os.walk(D):
    for f in fs:
        if not f.endswith('.html'): continue
        p=os.path.join(dp,f); rel=os.path.relpath(p,D)
        if rel.startswith(GEN) or rel=='404.html': continue
        h=open(p,encoding='utf-8').read(); o=h
        lang='en' if rel.startswith('en/') else 'ro'
        # antet
        m=re.search(r'(<body[^>]*>)(.*?)(<main\b)',h,re.S)
        if m and '<header' in m.group(2):
            h=h[:m.start(2)]+layout.header(lang)+h[m.end(2):]
        h=re.sub(r'<main\b(?![^>]*\bid=)',r'<main id="main"',h,count=1)
        # subsol: tot ce urmează după </main>, păstrând scripturile specifice paginii
        i=h.rfind('</main>')
        if i>0:
            tail=h[i+7:]
            if 'universal-footer' in tail or '<footer' in tail:
                srcs=[s for s in re.findall(r'<script[^>]*src="([^"]+)"[^>]*></script>',tail) if s.split('?')[0] not in KEEP_OUT]
                extra=''.join(f'<script src="{s}" defer></script>' for s in dict.fromkeys(srcs))
                h=h[:i+7]+layout.footer(lang)+extra+'</body></html>'
        # versiuni CSS/JS
        h=re.sub(r'/redesign\.css(\?v=[^"]*)?"',f'/redesign.css?v={layout.CSS_VER}"',h)
        h=re.sub(r'/style\.css(\?v=[^"]*)?"',f'/style.css?v={layout.CSS_VER}"',h)
        # program de lucru: luni–vineri până la 18:00
        h=h.replace('08:00–18:30','08:00–18:00').replace('08:00-18:30','08:00-18:00')
        h=re.sub(r'(Friday"\],"opens":"08:00","closes":)"18:30"',r'\1"18:00"',h)
        # Open Graph
        if 'og:title' not in h:
            t=re.search(r'<title>(.*?)</title>',h,re.S); d=re.search(r'<meta name="description" content="([^"]*)"',h); c=re.search(r'<link rel="canonical" href="https://fordcargo.ro([^"]*)"',h)
            if t and c:
                og=layout.og(lang,html.unescape(t.group(1).strip()),html.unescape(d.group(1)) if d else '',c.group(1))
                h=h.replace('</head>',og+'</head>',1)
        # formulări de marcă: „piese pentru camioane Ford”, nu „piese Ford”
        for a,b in FORD_TEXT: h=h.replace(a,b)
        # FAQPage doar pe pagina de întrebări frecvente (evităm date structurate duplicate)
        if rel!='intrebari-frecvente.html':
            h=re.sub(r'<script type="application/ld\+json">\{"@context":"https://schema.org","@type":"FAQPage".*?</script>','',h,flags=re.S)
        # logo în schema firmei
        if '"AutoPartsStore"]' in h and '"logo"' not in h:
            h=h.replace('"@type":["LocalBusiness","AutoPartsStore"],','"@type":["LocalBusiness","AutoPartsStore"],"logo":"https://fordcargo.ro/assets/eks-lkw-logo.jpg",',1)
        # profilul Google Business (Maps) în schema firmei
        MAPS='https://maps.google.com/?cid=3169278761931680726'
        if '"AutoPartsStore"]' in h and MAPS not in h:
            h=h.replace('"sameAs":[','"hasMap":"'+MAPS+'","sameAs":["'+MAPS+'",',1)
        # linkuri către adrese vechi de piesă (sufixe de furnizor) → adresa nouă
        h=re.sub(r'href="/piesa/([a-z0-9]+)/"',lambda m:f'href="/piesa/{PMAP.get(m.group(1),m.group(1))}/"',h)
        if rel=='catalog.html':
            for a,b in CAT_LABELS.items(): h=h.replace(f'/">{a}</a>',f'/">{b}</a>')
        if h!=o: open(p,'w',encoding='utf-8').write(h); n+=1
print('pagini actualizate',n)
