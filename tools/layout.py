"""Șablon comun pentru toate paginile generate (antet, subsol, <head>). Modifică aici o singură dată."""
import json,html
SITE='https://fordcargo.ro'
CSS_VER='22'
JS_VER='22'
CSP=("default-src 'self'; script-src 'self'; script-src-elem 'self' 'unsafe-inline'; script-src-attr 'none'; "
     "style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self'; connect-src 'self'; "
     "frame-src https://www.google.com https://maps.google.com; object-src 'none'; base-uri 'none'; form-action 'none'; upgrade-insecure-requests")
HOURS={'ro':'Luni–Vineri: 08:00–18:00<br>Sâmbătă: 08:00–15:30<br>Duminică: 08:30–13:00',
       'en':'Monday–Friday: 08:00–18:00<br>Saturday: 08:00–15:30<br>Sunday: 08:30–13:00'}
LOGO='<img class="vehicle" src="/assets/eks-lkw-logo-140.webp" alt="" width="70" height="69">'
LOGO_FOOT='<img class="vehicle" src="/assets/eks-lkw-logo-140.webp" alt="" width="56" height="55" loading="lazy">'
WM_LETTERS=[('M0 0H70V22H24V39H64V61H24V78H70V100H0Z',70),('M0 0H24V38L48 0H75L42 50L75 100H48L24 62V100H0Z',75),
 ('M70 0H10L0 10V46L10 56H46V78H0V100H60L70 90V54L60 44H24V22H70Z',70),None,('M0 0H24V78H70V100H0Z',70),
 ('M0 0H24V38L48 0H75L42 50L75 100H48L24 62V100H0Z',75),('M0 0H22L30 68L40 22H54L64 68L72 0H94L80 100H60L47 50L34 100H14Z',94)]
def wordmark(uid='h'):
    x=0;ps='';n=0
    for i,l in enumerate(WM_LETTERS):
        if l is None: x+=30;continue
        d,w=l; ps+=f'<g transform="translate({x} 0)"><path class="wm-l{" wm-g" if i>=4 else ""}" style="--i:{n}" d="{d}"/></g>'; x+=w+10; n+=1
    x-=10
    return (f'<svg class="wm" viewBox="-8 -6 {x+16} 112" aria-hidden="true" focusable="false"><g transform="skewX(-9)">'
            f'<mask id="wmc-{uid}" maskUnits="userSpaceOnUse" x="-30" y="-20" width="{x+60}" height="150"><rect x="-30" y="-20" width="{x+60}" height="150" fill="#fff"/><rect x="-30" y="47" width="{x+60}" height="5" fill="#000"/></mask>'
            f'<g mask="url(#wmc-{uid})">{ps}</g></g></svg>')
def brand_html(lang,cls='brand2',uid='h'):
    top='SINCE 1990 · ROMANIA' if lang=='en' else 'DIN 1990 · ROMÂNIA'
    sub='Parts for Ford Trucks' if lang=='en' else 'Piese pentru camioane Ford Trucks'
    href='/en/' if lang=='en' else '/'
    return (f'<span class="brand-sep" aria-hidden="true"></span><a class="{cls}" href="{href}" aria-label="EKS LKW — {sub}">'
            f'<span class="b-top">{top}</span><span class="b-name">{wordmark(uid)}</span><span class="b-sub">{sub}</span></a>')
SOCIAL=('<div class="social"><a href="https://www.facebook.com/PieseAutoCamioane/" target="_blank" rel="noopener" aria-label="facebook"><img src="/assets/facebook.svg" alt="" width="21" height="21"></a>'
        '<a href="https://www.instagram.com/ekslkw/" target="_blank" rel="noopener" aria-label="instagram"><img src="/assets/instagram.svg" alt="" width="21" height="21"></a>'
        '<a href="https://www.tiktok.com/@ekslkwsrl" target="_blank" rel="noopener" aria-label="tiktok"><img src="/assets/tiktok.svg" alt="" width="21" height="21"></a></div>')
def esc(s): return html.escape(s,quote=True)
def header(lang,alt_url=None):
    if lang=='ro':
        nav=('<a href="/">Acasă</a><details class="models-menu"><summary>Modele Ford</summary><div><a href="/piese-ford-cargo">Cargo</a><a href="/piese-ford-f-max">F-MAX și variante</a>'
             '<a href="/piese-ford-f-line">F-LINE</a><a href="/piese-ford-capete-tractor">Capete tractor</a><a href="/piese-ford-camioane-santier-basculante">Șantier / Basculante</a>'
             '<a href="/piese-ford-autospeciale">Autospeciale și suprastructuri</a></div></details><a href="/catalog">Catalog piese</a><a href="/cauta-piese">Caută piese</a>'
             '<a href="/despre-noi">Despre noi</a><a href="/contact">Contact</a><a class="nav-quote" href="/contact#cerere">Cere ofertă</a>')
        if alt_url: nav+=f'<a href="{alt_url}" hreflang="en" lang="en">EN</a>'
        top='PIESE ȘI ACCESORII PENTRU CAMIOANE ȘI CAPETE TRACTOR'; skip='Sari la conținut'; menu='Meniu ☰'; navl='Navigație principală'
    else:
        nav=('<a href="/en/">Home</a><details class="models-menu"><summary>Ford models</summary><div><a href="/en/ford-cargo-parts">Cargo</a><a href="/en/ford-f-max-parts">F-MAX and variants</a>'
             '<a href="/en/ford-f-line-parts">F-LINE</a><a href="/en/ford-tractor-unit-parts">Tractor units</a><a href="/en/ford-construction-tipper-parts">Construction / Tippers</a>'
             '<a href="/en/ford-special-vehicle-parts">Special vehicles and bodies</a></div></details><a href="/en/catalog">Parts catalogue</a><a href="/en/search">Search parts</a>'
             '<a href="/en/about">About us</a><a href="/en/contact">Contact</a><a class="nav-quote" href="/en/contact#cerere">Request a quote</a>')
        if alt_url: nav+=f'<a href="{alt_url}" hreflang="ro" lang="ro">RO</a>'
        top='PARTS AND ACCESSORIES FOR FORD TRUCKS AND TRACTOR UNITS'; skip='Skip to content'; menu='Menu ☰'; navl='Main navigation'
    return (f'<a class="skip" href="#main">{skip}</a><div class="topline"><div class="wrap">{top} <a href="tel:+40733357357">+40 733 357 357 </a></div></div>'
            f'<header class="wrap"><div class="brand-lockup">{LOGO}{brand_html(lang)}</div>'
            f'<button class="menu" aria-controls="navigation" aria-expanded="false">{menu}</button><nav id="navigation" aria-label="{navl}">{nav}</nav>{SOCIAL}</header>')
def footer(lang):
    if lang=='ro':
        t=dict(tag='Piese pentru întreaga gamă de camioane Ford Trucks și suprastructuri, la cerere. Un site EKS LKW PIESE AUTO.',prog='Program',info='Informații utile',
               links=[('/intrebari-frecvente','Întrebări frecvente'),('/ghiduri','Ghiduri'),('/politici/retur/','Retur'),('/politici/livrare/','Livrare și plată'),('/politici/garantie/','Garanție'),
                      ('/politici/termeni-si-conditii/','Termeni'),('/politici/confidentialitate/','Confidențialitate'),('/politici/cookies/','Cookies'),('/referinte/','Ghid de referințe')],
               reg='CUI RO36484785 · Nr. Registrul Comerțului J2016011620407',anpc='ANPC — Protecția Consumatorilor',sal='Soluționarea Alternativă a Litigiilor',pub='Achiziții publice',
               disc='FordCargo.ro este site-ul EKS LKW PIESE AUTO S.R.L., furnizor independent de piese pentru camioane Ford. Ford, Ford Cargo și F-MAX sunt mărci ale proprietarilor lor. Acest site nu este afiliat Ford Motor Company, Ford Otosan sau rețelei oficiale de dealeri Ford.',
               call='Sună acum',quick='Contact rapid',addr='Șoseaua Viilor 54, București 050152, România')
    else:
        t=dict(tag='Parts for the full Ford Trucks range and mounted bodies, on request. An EKS LKW PIESE AUTO website.',prog='Opening hours',info='Useful information',
               links=[('/en/faq','FAQ'),('/en/guides','Guides'),('/en/policies/returns/','Returns'),('/en/policies/delivery/','Delivery and payment'),('/en/policies/warranty/','Warranty'),('/en/policies/terms/','Terms'),
                      ('/en/policies/privacy/','Privacy'),('/en/policies/cookies/','Cookies'),('/en/references/','Part references')],
               reg='VAT RO36484785 · Trade Register J2016011620407',anpc='ANPC — Romanian consumer protection authority',sal='Alternative Dispute Resolution',pub='Public procurement',
               disc='FordCargo.ro is the website of EKS LKW PIESE AUTO S.R.L., an independent supplier of parts for Ford trucks. Ford, Ford Cargo and F-MAX are trademarks of their respective owners. This site is not affiliated with Ford Motor Company, Ford Otosan or the official Ford dealer network.',
               call='Call now',quick='Quick contact',addr='Șoseaua Viilor 54, Bucharest 050152, Romania')
    links=''.join(f'<a href="{u}">{n}</a>' for u,n in t['links'])
    return (f'<footer class="universal-footer"><div class="wrap footer-grid"><div><div class="brand-lockup footer-lockup">'+LOGO_FOOT+brand_html(lang,uid='f')+f'</div><p>{t["tag"]}</p>'
            f'<a href="https://eurokolben.ro" target="_blank" rel="noopener">EKS LKW PIESE AUTO S.R.L. · eurokolben.ro</a></div><div><div class="business-hours"><strong>{t["prog"]}</strong><p>{HOURS[lang]}</p></div>'
            f'<strong>Contact</strong><a href="tel:+40733357357">+40 733 357 357</a><a href="tel:+40745820894">+40 745 820 894</a><a href="mailto:office@eurokolben.ro">EKS LKW PIESE AUTO S.R.L.<br>office@eurokolben.ro</a>'
            f'<p>{t["addr"]}<br>{t["reg"]}</p></div><div><strong>{t["info"]}</strong>{links}</div></div>'
            f'<div class="wrap badges"><a class="institution anpc-institution" href="https://anpc.ro/" target="_blank" rel="noopener" aria-label="ANPC"><img src="/assets/anpc-logo.png" alt="{t["anpc"]}" width="228" height="107" loading="lazy"></a>'
            f'<a class="institution sal-institution" href="https://reclamatiisal.anpc.ro/" target="_blank" rel="noopener" aria-label="SAL — ANPC"><img src="/assets/anpc-sal.png" alt="{t["sal"]}" width="201" height="50" loading="lazy"></a>'
            f'<div class="institution seap-institution"><img src="/assets/seap-official.png" alt="" width="42" height="60" loading="lazy"><span><strong>SEAP / SICAP</strong><small>{t["pub"]}</small></span></div></div>'
            f'<div class="wrap footer-disclaimer"><p>{t["disc"]}</p></div><div class="wrap copyright">© 2026 EKS LKW PIESE AUTO S.R.L.</div></footer>'
            f'<a class="whatsapp" href="https://wa.me/40733357357" target="_blank" rel="noopener" aria-label="WhatsApp">WhatsApp</a>'
            f'<div class="mobile-contact-bar" aria-label="{t["quick"]}"><a href="tel:+40733357357">{t["call"]}</a><a href="https://wa.me/40733357357" target="_blank" rel="noopener">WhatsApp</a></div>'
            f'<script src="/site.js?v={JS_VER}" defer></script><script src="/privacy-controls.js" defer></script>')
def og(lang,title,desc,path,ogtype='website'):
    return (f'<meta property="og:type" content="{ogtype}"><meta property="og:site_name" content="EKS LKW — piese pentru camioane Ford">'
            f'<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}">'
            f'<meta property="og:url" content="{SITE}{path}"><meta property="og:image" content="{SITE}/assets/og-image.jpg">'
            f'<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">'
            f'<meta property="og:locale" content="{"ro_RO" if lang=="ro" else "en_GB"}"><meta name="twitter:card" content="summary_large_image">')
def breadcrumb_ld(items):
    return {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":i+1,"name":n,"item":SITE+u} for i,(n,u) in enumerate(items)]}
def page(lang,title,desc,path,main,crumbs=None,robots='index,follow',alt=None,ld=None):
    """alt = (lang, path) al versiunii în cealaltă limbă."""
    lds=[]
    if crumbs: lds.append(breadcrumb_ld(crumbs))
    if ld: lds.append(ld)
    ldh=''.join(f'<script type="application/ld+json">{json.dumps(x,ensure_ascii=False,separators=(",",":"))}</script>' for x in lds)
    alth=''
    if alt:
        alth=(f'<link rel="alternate" hreflang="{lang}" href="{SITE}{path}"><link rel="alternate" hreflang="{alt[0]}" href="{SITE}{alt[1]}">')
    return (f'<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta http-equiv="Content-Security-Policy" content="{CSP}">'
            f'<meta name="referrer" content="no-referrer"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)}</title>'
            f'<meta name="description" content="{esc(desc)}"><link rel="icon" href="/assets/favicon-96.png" sizes="96x96"><link rel="apple-touch-icon" sizes="180x180" href="/assets/favicon-180.png">'
            f'<link rel="stylesheet" href="/style.css?v={CSS_VER}"><link rel="stylesheet" href="/redesign.css?v={CSS_VER}"><meta name="robots" content="{robots}">'
            f'<link rel="canonical" href="{SITE}{path}">{alth}{og(lang,title,desc,path)}{ldh}</head>'
            f'<body>{header(lang,alt[1] if alt else None)}<main id="main" class="wrap catalog-detail">{main}</main>{footer(lang)}</body></html>')
def crumbs_html(items,lang):
    lab='Fir de navigare' if lang=='ro' else 'Breadcrumb'
    parts=[]
    for i,(n,u) in enumerate(items):
        parts.append(f'<span aria-current="page">{esc(n)}</span>' if i==len(items)-1 else f'<a href="{u}">{esc(n)}</a>')
    return f'<nav class="breadcrumbs" aria-label="{lab}">'+'<span aria-hidden="true"> / </span>'.join(parts)+'</nav>'
