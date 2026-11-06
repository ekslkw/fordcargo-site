"""Generează paginile catalogului din data/catalog.json.
Rulare:  python3 tools/build_catalog.py      (din rădăcina depozitului)
Generează: dist/piesa/*, dist/categorie/*, dist/referinte/*, dist/en/references/*, dist/assets/search-data.json"""
import json,os,re,shutil,sys,collections
from urllib.parse import quote
sys.path.insert(0,os.path.dirname(__file__)); from layout import page,esc,crumbs_html
from classify import base as ford_base
D='dist'
GROUPS={ # cheie: (RO, EN, descriere RO, descriere EN)
 'motor':('Motor și ungere','Engine and lubrication','pistoane, cămăși, chiulase, garnituri, pompe de ulei, curele și componente de motor','pistons, liners, cylinder heads, gaskets, oil pumps, belts and engine components'),
 'transmisie':('Transmisie și ambreiaj','Transmission and clutch','ambreiaje, cutii de viteze, sincroane, punți spate, planetare și prize de putere (PTO)','clutches, gearboxes, synchronisers, rear axles, axle shafts and PTO units'),
 'franare':('Frânare','Braking','compresoare de aer, uscătoare, supape, cilindri, tamburi, saboți și senzori ABS/EBS','air compressors, air dryers, valves, brake chambers, drums, shoes and ABS/EBS sensors'),
 'suspensie':('Suspensie și roți','Suspension and wheels','arcuri, perne de aer, amortizoare, bare stabilizatoare, butuci și prezoane de roată','springs, air bellows, shock absorbers, anti-roll bars, hubs and wheel studs'),
 'directie':('Direcție','Steering','casete de direcție, bare, capete de bară, fuzete și pivoți','steering boxes, rods, tie-rod ends, knuckles and king pins'),
 'electric':('Electrică și iluminare','Electrical and lighting','alternatoare, demaroare, senzori, comutatoare, relee, faruri și lămpi','alternators, starters, sensors, switches, relays, headlamps and lamps'),
 'racire':('Răcire','Cooling','radiatoare, pompe de apă, termostate, ventilatoare, răcitoare de ulei și furtunuri','radiators, water pumps, thermostats, fans, oil coolers and hoses'),
 'cabina':('Cabină și caroserie','Cab and body','oglinzi, ștergătoare, panouri, spoilere, uși, scaune, grile și elemente de cabină','mirrors, wipers, panels, spoilers, doors, seats, grilles and cab components'),
 'filtre':('Filtre și întreținere','Filters and service','filtre de ulei, combustibil, aer, habitaclu și consumabile de revizie','oil, fuel, air and cabin filters and service consumables'),
 'turbo':('Turbo, admisie și evacuare','Turbo, intake and exhaust','turbocompresoare, intercoolere, furtunuri de admisie, galerii și componente de evacuare','turbochargers, intercoolers, intake hoses, manifolds and exhaust components'),
 'alimentare':('Alimentare, injecție și AdBlue','Fuel, injection and AdBlue','injectoare, pompe de combustibil, rezervoare și componente SCR / AdBlue','injectors, fuel pumps, tanks and SCR / AdBlue components'),
 'climatizare':('Încălzire și climatizare','Heating and air conditioning','compresoare AC, condensatoare, conducte, încălzire habitaclu și ventilație','A/C compressors, condensers, pipes, cab heating and ventilation'),
 'alte':('Șasiu, fixări și alte componente','Chassis, fasteners and other parts','lonjeroane, traverse de șasiu, șuruburi, piulițe, șaibe, garnituri și alte piese generale','chassis side members, crossmembers, bolts, nuts, washers, seals and other general parts'),
}
ORDER=list(GROUPS)
PER_CAT=100; PER_REF=80
def slug(s): return re.sub(r'[^a-z0-9]','',s.replace('İ','').replace('ı','').lower())
def codekey(s): return slug(s)
def ro_quote_link(name,codes): return '/contact?part='+quote(f'{name} — {codes}',safe='')+'#cerere'
data=json.load(open('data/catalog.json'))['records']
# --- pagini piese: o pagină pentru fiecare cod (slug) unic
pages=collections.OrderedDict()
for x in data:
    for f in x['refs']:
        s=slug(f)
        if s and s not in pages: pages[s]=(f,x)
by_group=collections.defaultdict(list)
for s,(f,x) in pages.items(): by_group[x['group']].append((s,f,x))
for g in by_group: by_group[g].sort(key=lambda t:t[0])
rec_group=collections.defaultdict(list)
for x in data: rec_group[x['group']].append(x)
for g in rec_group: rec_group[g].sort(key=lambda x:codekey(x['refs'][0]))
# pagina (RO/EN references) pe care apare fiecare fișă
ref_page={}
for g,lst in rec_group.items():
    for i,x in enumerate(lst): ref_page[x['id']]=i//PER_REF+1
# --- curăță directoarele generate
for d in ['piesa','categorie','referinte','en/references']:
    shutil.rmtree(os.path.join(D,d),ignore_errors=True)
def write(path,content):
    fp=os.path.join(D,path.strip('/'),'index.html') if path.endswith('/') else os.path.join(D,path.strip('/'))
    os.makedirs(os.path.dirname(fp),exist_ok=True); open(fp,'w',encoding='utf-8').write(content)

FORD_GRP=[(1000,1999,'roți și butuci'),(2000,2999,'sistemul de frânare'),(3000,3999,'direcție și punte față'),(4000,4999,'punte spate și transmisie finală'),
 (5000,5999,'suspensie, șasiu și evacuare'),(6000,6999,'motor'),(7000,7999,'cutie de viteze și ambreiaj'),(8000,8999,'răcire'),(9000,9999,'alimentare și emisii'),
 (10000,15999,'echipament electric'),(16000,17999,'caroserie față, bare de protecție și oglinzi'),(18000,19999,'încălzire și climatizare'),(20000,29999,'caroserie și cabină')]
def ford_group_note(code):
    b=ford_base(code)
    if not b: return ''
    m=re.match(r'(\d+)([A-Z]*)',b)
    if not m: return ''
    dig,let=m.groups(); n=int(dig)
    if let and len(dig)<=2: n*=1000
    for lo,hi,lab in FORD_GRP:
        if lo<=n<=hi:
            return f'În sistemul de numerotare Ford, codul de bază <b>{esc(b)}</b> face parte din grupa {lo//1000 if lo<10000 else str(lo//1000)+"–"+str(hi//1000)}xxx, care cuprinde în general piese pentru {lab}.'
    return ''
GENERIC=('Piesă pentru camioane Ford','Componentă ')
# --- pagini piesă
for g,lst in by_group.items():
    gro=GROUPS[g][0]
    n=len(lst)
    for i,(s,f,x) in enumerate(lst):
        path=f'/piesa/{s}/'; name=x['ro']
        crumbs=[('Acasă','/'),('Catalog piese','/catalog'),(gro,f'/categorie/{g}/'),(f,path)]
        others=[r for r in x['refs'] if r!=f]
        rel=[lst[(i+k)%n] for k in range(1,7) if n>1 and (i+k)%n!=i]
        seen=set(); rel=[t for t in rel if not (t[0] in seen or seen.add(t[0]))]
        models=', '.join(x['models'])
        en_url=f"/en/references/{g}/{ref_page[x['id']]}/#piesa-{x['id']}"
        dl=f'<dt>Cod / referință</dt><dd>{esc(f)}</dd><dt>Cod fără separatori</dt><dd>{esc(re.sub(r"[^A-Za-z0-9İ]","",f))}</dd><dt>Categorie</dt><dd><a href="/categorie/{g}/">{esc(gro)}</a></dd>'
        if others: dl+='<dt>Referințe asociate</dt><dd>'+' · '.join(f'<a href="/piesa/{slug(o)}/">{esc(o)}</a>' for o in others)+'</dd>'
        if models: dl+=f'<dt>Aplicație</dt><dd>{esc(models)}</dd>'
        dl+='<dt>Producător</dt><dd>Original Ford sau aftermarket — se precizează în ofertă</dd>'
        dl+=f'<dt>Denumire în engleză</dt><dd><a href="{en_url}" hreflang="en">{esc(x["en"])}</a></dd>'
        note=ford_group_note(f)
        kind='Cod Ford' if 'C46' in f or 'C44' in f else ('Cod T' if re.fullmatch(r'T\d{5,8}',f.replace(' ','')) else 'Cod de referință')
        intro=f'{kind} <b>{esc(f)}</b>: {esc(name.lower() if name[:1].isupper() and not name[:2].isupper() else name)}, din grupa <a href="/categorie/{g}/">{esc(gro.lower())}</a>.'
        if others: intro+=f' Aceeași fișă de catalog include și {"referința" if len(others)==1 else "referințele"} {", ".join(esc(o) for o in others)}.'
        main=(crumbs_html(crumbs,'ro')+f'<div class="eyebrow">REFERINȚĂ CATALOG · {esc(gro.upper())}</div>'
              f'<h1>{esc(f)} — {esc(name)}</h1>'
              f'<p class="reference-note">{intro}</p>'
              +(f'<p>{note}</p>' if note else '')+
              f'<dl>{dl}</dl>'
              f'<p>Disponibilitatea, producătorul și prețul se confirmă în ofertă. Verificăm aplicația după cod sau după seria de șasiu (VIN) înainte de livrare.</p>'
              f'<p class="detail-actions"><a class="button" href="{ro_quote_link(name,f)}">Cere ofertă</a> <a class="button secondary" href="https://wa.me/40733357357?text={quote("Bună ziua! Doresc o ofertă pentru "+f+" — "+name,safe="")}" target="_blank" rel="noopener">Întreabă pe WhatsApp</a></p>')
        if rel:
            main+='<h2>Alte piese din categoria '+esc(gro)+'</h2><ul class="related-codes">'+''.join(f'<li><a href="/piesa/{t[0]}/">{esc(t[1])} — {esc(t[2]["ro"])}</a></li>' for t in rel)+'</ul>'
        title=f'{f} — {name} | EKS LKW'
        desc=f'{name} ({f}) pentru camioane Ford Trucks. Ofertă la cerere de la EKS LKW București, cu verificare după cod sau VIN.'
        if len(desc)>158: desc=f'{name} ({f}) pentru camioane Ford Trucks. Ofertă la cerere de la EKS LKW București.'
        if len(desc)>158: desc=desc[:155].rsplit(' ',1)[0]+'…'
        robots='noindex,follow' if name.startswith(GENERIC) else 'index,follow'
        write(path,page('ro',title,desc,path,main,crumbs,robots=robots))
# --- pagini categorie (RO, listă de coduri)
for g in ORDER:
    lst=by_group.get(g,[])
    gro,gen,dro,den=GROUPS[g]; np=max(1,-(-len(lst)//PER_CAT))
    for p in range(1,np+1):
        path=f'/categorie/{g}/' if p==1 else f'/categorie/{g}/{p}/'
        sl=lst[(p-1)*PER_CAT:p*PER_CAT]
        crumbs=[('Acasă','/'),('Catalog piese','/catalog'),(gro,f'/categorie/{g}/')]
        if p>1: crumbs.append((f'Pagina {p}',path))
        nav=[]
        if p>1: nav.append(f'<a href="{"/categorie/"+g+"/" if p==2 else f"/categorie/{g}/{p-1}/"}">← Pagina anterioară</a>')
        nav.append(f'<span>Pagina {p} / {np}</span>')
        if p<np: nav.append(f'<a href="/categorie/{g}/{p+1}/">Pagina următoare →</a>')
        main=(crumbs_html(crumbs,'ro')+f'<h1>{esc(gro)} — piese pentru camioane Ford{"" if p==1 else f" (pagina {p})"}</h1>'
              f'<p>{len(lst)} referințe pentru camioane Ford Trucks: {dro}. Piesele sunt disponibile la cerere, originale sau aftermarket; aplicația se confirmă în ofertă.</p>'
              '<ul class="reference-list">'+''.join(f'<li><a href="/piesa/{s}/">{esc(f)} — {esc(x["ro"])}</a></li>' for s,f,x in sl)+'</ul>'
              f'<nav class="pagination reference-pagination" aria-label="Pagini">{"".join(nav)}</nav>'
              '<p><a href="/catalog">Toate categoriile ↗</a> · <a href="/cauta-piese">Caută după cod ↗</a></p>')
        sfx='' if p==1 else f' — pagina {p}'
        title=f'{gro} pentru camioane Ford{sfx} | EKS LKW'
        desc=(f'{gro} pentru camioane Ford Trucks{sfx}: {dro}.')
        if len(desc)>158: desc=desc[:155].rsplit(' ',1)[0]+'…'
        write(path,page('ro',title,desc,path,main,crumbs))
# --- tabele de referințe RO / EN
for lang in ['ro','en']:
    base='/referinte/' if lang=='ro' else '/en/references/'
    altbase='/en/references/' if lang=='ro' else '/referinte/'
    T=dict(ro=dict(part='Piesă',refs='Referințe',app='Aplicație',q='Ofertă',ask='Cere ofertă ↗',conf='Ford camion — aplicație de confirmat',kind='Referință de catalog',
                   prev='← Înapoi',next='Înainte →',pg='Pagina',all='Toate grupele de piese ↗',eyebrow='PIESE CAMIOANE FORD',home='Acasă',idx='Ghid de referințe',
                   intro='Consultă referințele tehnice și solicită o ofertă pentru camionul tău Ford. Opțiunile originale sau aftermarket, disponibilitatea, compatibilitatea și termenul se confirmă în ofertă.',
                   note='Referințele grupate într-o fișă sunt alternative publicate pentru aceeași piesă. Nu stabilesc o echivalență universală între fiecare cod. O referință de catalog nu confirmă proveniența originală sau stocul curent.',
                   cnt='fișe'),
             en=dict(part='Part',refs='References',app='Application',q='Quote',ask='Request quote ↗',conf='Ford truck — application to be confirmed',kind='Catalogue reference',
                   prev='← Previous',next='Next →',pg='Page',all='All part groups ↗',eyebrow='FORD TRUCK PARTS',home='Home',idx='Part references',
                   intro='Browse technical part references and request a quotation for your Ford truck. Original or aftermarket options, availability, compatibility and lead time are confirmed in the offer.',
                   note='References grouped in a single entry are alternatives published for the same part. They do not establish universal one-to-one interchangeability. Catalogue references do not establish genuine origin or live stock.',
                   cnt='entries'))[lang]
    cards=''
    for g in ORDER:
        lst=rec_group.get(g,[])
        if not lst: continue
        gname=GROUPS[g][0 if lang=='ro' else 1]; gdesc=GROUPS[g][2 if lang=='ro' else 3]
        cards+=f'<a href="{base}{g}/1/"><b>{esc(gname)}</b><span>{len(lst)} {T["cnt"]} ↗</span></a>'
        np=-(-len(lst)//PER_REF)
        for p in range(1,np+1):
            path=f'{base}{g}/{p}/'
            rows=''
            for x in lst[(p-1)*PER_REF:p*PER_REF]:
                nm=x[lang]; codes=', '.join(x['refs'])
                code_html=' · '.join(f'<a href="/piesa/{slug(r)}/">{esc(r)}</a>' for r in x['refs'])
                rows+=(f'<tr id="piesa-{x["id"]}"><td><b>{esc(nm)}</b><small>{T["kind"]}</small></td><td class="code">{code_html}</td>'
                       f'<td>{esc(", ".join(x["models"])) or T["conf"]}</td><td><a href="{ro_quote_link(nm,codes)}">{T["ask"]}</a></td></tr>')
            nav=[]
            if p>1: nav.append(f'<a href="{base}{g}/{p-1}/">{T["prev"]}</a>')
            nav.append(f'<span>{T["pg"]} {p} / {np}</span>')
            if p<np: nav.append(f'<a href="{base}{g}/{p+1}/">{T["next"]}</a>')
            crumbs=[(T['home'],'/'),(T['idx'],base),(gname,f'{base}{g}/1/')]
            if p>1: crumbs.append((f'{T["pg"]} {p}',path))
            main=(crumbs_html(crumbs,lang)+f'<div class="eyebrow dark">{T["eyebrow"]}</div><h1>{esc(gname)}{"" if p==1 else f" — {T['pg'].lower()} {p}"}</h1><p>{T["intro"]}</p><p>{T["note"]}</p>'
                  f'<div class="reference-table"><table><thead><tr><th>{T["part"]}</th><th>{T["refs"]}</th><th>{T["app"]}</th><th>{T["q"]}</th></tr></thead><tbody>{rows}</tbody></table></div>'
                  f'<nav class="reference-pagination" aria-label="{T["pg"]}">{"".join(nav)}</nav><p><a href="{base}">{T["all"]}</a></p>')
            if lang=='ro':
                title=f'Referințe piese — {gname} · {p} | EKS LKW'; desc=f'Referințe {gname.lower()} pentru camioane Ford Trucks (pagina {p} din {np}): {gdesc}. Cere ofertă la EKS LKW București.'
            else:
                title=f'{gname} part references · {p} | EKS LKW'; desc=f'{gname} references for Ford Trucks (page {p} of {np}): {gdesc}. Request a quote from EKS LKW, Bucharest.'
            write(path,page(lang,title,desc,path,main,crumbs,alt=('en' if lang=='ro' else 'ro',f'{altbase}{g}/{p}/')))
    # index
    if lang=='ro':
        main=(crumbs_html([('Acasă','/'),('Ghid de referințe','/referinte/')],'ro')+'<div class="eyebrow dark">CATALOG TEHNIC</div><h1>Referințe de piese pentru camioane Ford</h1>'
              '<p>Un ghid de referințe pentru identificarea pieselor și solicitarea unei oferte individuale. Alege o grupă sau caută după un cod tehnic ori o referință T.</p>'
              f'<a class="button" href="/cauta-piese">Caută toate codurile ↗</a><div class="reference-directory">{cards}</div>')
        write('/referinte/',page('ro','Ghid de referințe | EKS LKW','Ghid de referințe pentru piese de camioane Ford Trucks, pe grupe: motor, transmisie, frânare, suspensie, cabină și altele. Cere ofertă la EKS LKW București.','/referinte/',main,[('Acasă','/'),('Ghid de referințe','/referinte/')],alt=('en','/en/references/')))
    else:
        main=(crumbs_html([('Home','/'),('Part references','/en/references/')],'en')+'<div class="eyebrow dark">TECHNICAL CATALOGUE</div><h1>Part references for Ford trucks</h1>'
              '<p>A reference guide for identifying parts and requesting an individual quotation. Choose a group or search by technical code or T reference.</p>'
              f'<a class="button" href="/cauta-piese">Search all codes ↗</a><div class="reference-directory">{cards}</div>')
        write('/en/references/',page('en','Part references | EKS LKW','Ford Trucks part references by group: engine, transmission, braking, suspension, cab and more. Request a quote from EKS LKW, Bucharest.','/en/references/',main,[('Home','/'),('Part references','/en/references/')],alt=('ro','/referinte/')))
# --- date căutare (format compact v2: [id, ro, en, coduri "a|b", modele "a|b", indice grupă, pagina EN, slug pagină RO])
gi={g:i for i,g in enumerate(ORDER)}
rows=[[x['id'],x['ro'],x['en'],'|'.join(x['refs']),'|'.join(x['models']),gi[x['group']],ref_page[x['id']],slug(x['refs'][0])] for x in data]
json.dump({'v':2,'g':ORDER,'r':rows},open(os.path.join(D,'assets/search-data.json'),'w'),ensure_ascii=False,separators=(',',':'))
print('piese',len(pages),'| categorii',{g:len(by_group.get(g,[])) for g in ORDER})

# --- pagina 404
main=('<h1>Pagina nu a fost găsită</h1><p>Adresa nu mai există sau a fost mutată. Caută piesa după cod sau contactează echipa EKS LKW.</p>'
      '<p class="detail-actions"><a class="button" href="/cauta-piese">Caută după cod</a> <a class="button secondary" href="/catalog">Catalog piese</a> <a class="button secondary" href="tel:+40733357357">Sună: +40 733 357 357</a></p>')
open(os.path.join(D,'404.html'),'w',encoding='utf-8').write(page('ro','Pagina nu a fost găsită | EKS LKW','Pagina căutată nu a fost găsită pe FordCargo.ro.','/404.html',main,robots='noindex'))
