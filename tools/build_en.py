"""Versiunea în engleză a paginilor principale (dist/en/...), generată din paginile RO + tools/en_text.py.
Se rulează după fix_static și build_ghiduri. Paginile RO primesc legătura EN și hreflang."""
import os,re,sys,html,json
sys.path.insert(0,os.path.dirname(__file__))
import layout
from en_text import T,RO_CODE_FIX
D='dist'; SITE='https://fordcargo.ro'
PAGES={  # fișier RO -> (cale RO, cale EN, fișier EN)
 'index.html':('/','/en/','en/index.html'),
 'despre-noi.html':('/despre-noi','/en/about','en/about.html'),
 'contact.html':('/contact','/en/contact','en/contact.html'),
 'catalog.html':('/catalog','/en/catalog','en/catalog.html'),
 'cauta-piese.html':('/cauta-piese','/en/search','en/search.html'),
 'intrebari-frecvente.html':('/intrebari-frecvente','/en/faq','en/faq.html'),
 'ghiduri.html':('/ghiduri','/en/guides','en/guides.html'),
}
ENSLUG={'cargo':'ford-cargo-parts','f-max':'ford-f-max-parts','f-max-l':'ford-f-max-l-parts','f-max-midilli':'ford-f-max-midilli-parts',
 'f-max-lowliner':'ford-f-max-lowliner-parts','f-line':'ford-f-line-parts','f-line-rutiere':'ford-f-line-road-parts','f-line-constructii':'ford-f-line-construction-parts',
 'f-line-electrice':'ford-f-line-e-parts','capete-tractor':'ford-tractor-unit-parts','camioane-santier-basculante':'ford-construction-tipper-parts',
 'autospeciale':'ford-special-vehicle-parts','autospeciale-pompieri':'ford-fire-truck-parts','camioane-de-gunoi':'ford-refuse-truck-parts',
 'cisterne-apa':'ford-water-tanker-parts','cisterne-combustibil':'ford-fuel-tanker-parts','utilaje-deszapezire':'ford-snow-clearing-truck-parts'}
for f in sorted(os.listdir(D)):
    m=re.fullmatch(r'piese-ford-(.+)\.html',f)
    if m:
        en=ENSLUG[m.group(1)]
        PAGES[f]=(f'/piese-ford-{m.group(1)}',f'/en/{en}',f'en/{en}.html')
LINK={ro:en for _,(ro,en,_) in PAGES.items()}
LINK.update({'/ghid/identificare-piesa-ford-cargo':'/en/guides/finding-the-right-ford-cargo-part/','/ghid/cod-piesa-ford-prefix-baza-sufix':'/en/guides/reading-a-ford-part-number/','/ghid/coduri-t-finis-si-coduri-ford':'/en/guides/t-finis-and-ford-part-numbers/'})
GROUPS=['motor','transmisie','franare','suspensie','directie','electric','racire','cabina','filtre','turbo','alimentare','climatizare','alte']

def map_href(u):
    base,frag=(u.split('#',1)+[''])[:2]; frag='#'+frag if frag else ''
    b=base.rstrip('/') or '/'
    if b in LINK: return LINK[b]+frag
    if b.endswith('.html') and b[:-5] in LINK: return LINK[b[:-5]]+frag
    m=re.fullmatch(r'/categorie/([a-z]+)',b)
    if m and m.group(1) in GROUPS: return f'/en/references/{m.group(1)}/'+frag
    if b=='/politici/confidentialitate': return '/en/policies/privacy/'+frag
    return u
def tr_text(s):
    k=s.strip()
    if k in T:
        lead=s[:len(s)-len(s.lstrip())]; tail=s[len(s.rstrip()):]
        return lead+T[k]+tail
    return s

missing=set()
for rof,(rop,enp,enf) in PAGES.items():
    h=open(f'{D}/{rof}',encoding='utf-8').read()
    for a,b in RO_CODE_FIX.items(): h=h.replace(a,b)
    # RO: legătura către EN + hreflang
    ro=h
    ro=re.sub(r'<link rel="alternate" hreflang="[^"]*" href="[^"]*">','',ro)
    ro=ro.replace('</head>',f'<link rel="alternate" hreflang="ro" href="{SITE}{rop}"><link rel="alternate" hreflang="en" href="{SITE}{enp}"><link rel="alternate" hreflang="x-default" href="{SITE}{rop}"></head>',1)
    m=re.search(r'<a class="skip".*?</header>',ro,re.S)
    if m: ro=ro[:m.start()]+layout.header('ro',enp)+ro[m.end():]
    open(f'{D}/{rof}','w',encoding='utf-8').write(ro)
    # EN
    e=ro.replace('<html lang="ro"','<html lang="en"')
    i=e.find('<main'); j=e.rfind('</main>')
    head,main,tail=e[:i],e[i:j],e[j:]
    def txt(mm):
        s=mm.group(1)
        if s.strip() and re.search('[A-Za-zĂÂÎȘȚăâîșț]{2}',s) and s.strip() not in T: missing.add(s.strip())
        return '>'+tr_text(s)+'<'
    main=re.sub(r'>([^<>]+)<',txt,main)
    main=re.sub(r'(\s(?:alt|placeholder|aria-label|title)=")([^"]+)(")',lambda mm:mm.group(1)+html.escape(T.get(html.unescape(mm.group(2)).strip(),html.unescape(mm.group(2))),quote=True)+mm.group(3),main)
    main=re.sub(r'href="(/[^"]*)"',lambda mm:f'href="{map_href(mm.group(1))}"',main)
    # head: titlu, descriere, canonical, og, json-ld
    def attr(mm): return mm.group(1)+html.escape(T.get(html.unescape(mm.group(2)),html.unescape(mm.group(2))),quote=True)+mm.group(3)
    head=re.sub(r'(<title>)(.*?)(</title>)',attr,head,flags=re.S)
    head=re.sub(r'(<meta (?:name="description"|property="og:(?:title|description)"|name="twitter:(?:title|description)") content=")([^"]*)(")',attr,head)
    head=head.replace(f'<link rel="canonical" href="{SITE}{rop}"',f'<link rel="canonical" href="{SITE}{enp}"')
    head=re.sub(r'(<meta property="og:url" content=")[^"]*',lambda mm:mm.group(1)+SITE+enp,head)
    head=re.sub(r'(<meta property="og:locale" content=")[^"]*',r'\1en_GB',head)
    def ld(mm):
        try: d=json.loads(mm.group(1))
        except Exception: return mm.group(0)
        def walk(x):
            if isinstance(x,dict): return {k:walk(v) for k,v in x.items()}
            if isinstance(x,list): return [walk(v) for v in x]
            if isinstance(x,str):
                if x in T: return T[x]
                if x.startswith(SITE): return SITE+map_href(x[len(SITE):] or '/')
            return x
        return '<script type="application/ld+json">'+json.dumps(walk(d),ensure_ascii=False,separators=(',',':'))+'</script>'
    head=re.sub(r'<script type="application/ld\+json">(.*?)</script>',ld,head,flags=re.S)
    m=re.search(r'<a class="skip".*?</header>',head,re.S)
    if m: head=head[:m.start()]+layout.header('en',rop)+head[m.end():]
    k=tail.find('</main>')+7; t2=tail[k:]
    fs=re.search(r'<footer.*?</footer>',t2,re.S)
    if fs: t2=t2[:fs.start()]+re.search(r'<footer.*?</footer>',layout.footer('en'),re.S).group(0)+t2[fs.end():]
    out=head+main+tail[:k]+t2
    os.makedirs(os.path.dirname(f'{D}/{enf}'),exist_ok=True)
    open(f'{D}/{enf}','w',encoding='utf-8').write(out)
print('pagini EN',len(PAGES))
if missing: print('netraduse:',len(missing)); [print('  ',x[:100]) for x in sorted(missing)[:40]]
