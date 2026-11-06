"""Ghiduri (blog): pagina /ghiduri + articole în /ghid/<slug>/.
Textele sunt scrise manual; se modifică aici și se rulează scriptul (după fix_static)."""
import os,re,sys
sys.path.insert(0,os.path.dirname(__file__))
from layout import page,esc,crumbs_html,SITE
D='dist'
ORG={"@type":"Organization","name":"EKS LKW Piese Auto S.R.L.","url":SITE+"/"}

ART=[
dict(slug='identificare-piesa-ford-cargo',date='2026-11-06',
 title='Cum găsești piesa potrivită pentru un Ford Cargo',
 desc='Ce date să pregătești înainte să ceri o piesă pentru Ford Cargo: codul de pe piesă, poziția de montaj, VIN-ul și fotografiile care ajută la identificare.',
 lead='Două camioane Ford Cargo din același an pot avea motor, cutie sau punte diferite. De aceea, la telefon, prima noastră întrebare nu este „ce model aveți?”, ci „ce scrie pe piesă?”.',
 body='''
<h2>1. Începe cu piesa veche</h2>
<p>Codul de pe piesa demontată este cea mai sigură informație. Pe piesele Ford el arată de obicei așa: <b>7C46 7550 BA</b> (un disc de ambreiaj) sau <b>CC46 2L324 AA</b> (o supapă de frână de parcare). Copiază-l complet, cu literele de la final, și fă o fotografie clară a etichetei sau a marcajului ștanțat.</p>
<p>Dacă pe piesă apar mai multe numere, trimite-le pe toate. Unul poate fi codul Ford, altul codul producătorului care a fabricat piesa, altul un număr de lot. Noi le separăm la verificare.</p>
<h2>2. Spune unde este montată</h2>
<p>Pentru frâne, suspensie și direcție contează puntea și partea: față sau spate, stânga sau dreapta. Pentru o piesă electrică fotografiază și mufa, numărul de pini se vede mai ușor într-o poză decât într-o descriere. Pentru furtunuri și conducte ajută o fotografie cu ambele capete.</p>
<h2>3. VIN-ul ajută când codul lipsește</h2>
<p>Seria de șasiu (VIN) este în talonul camionului și pe plăcuța din cabină. Cu ea putem verifica configurația din fabrică atunci când piesa nu mai are etichetă sau când a fost deja înlocuită cu una de altă proveniență. În formularul de pe site câmpul VIN este opțional. Dacă trimiți o poză cu talonul, acoperă datele proprietarului; ne trebuie doar seria de șasiu.</p>
<h2>4. Suprastructura are altă plăcuță</h2>
<p>Basculanta, macaraua, cisterna sau compactorul de gunoi nu sunt fabricate de Ford. Pentru piesele lor ne trebuie producătorul echipamentului și seria de pe plăcuța lui, nu VIN-ul camionului.</p>
<h2>5. Cere confirmarea înainte de comandă</h2>
<p>În ofertă precizăm codul exact, producătorul piesei (original Ford sau aftermarket), termenul de livrare și prețul. Dacă diferă sufixul sau există o variantă înlocuitoare, îți spunem înainte să comanzi.</p>
<p class="note">Nu ai codul? Scrie-ne ce piesă cauți, pe ce camion și cum arată. Pornim de acolo și îți cerem ce mai lipsește.</p>
'''),
dict(slug='cod-piesa-ford-prefix-baza-sufix',date='2026-11-06',
 title='Cum se citește un cod de piesă Ford: prefix, bază și sufix',
 desc='Un cod Ford precum 3C46 7548 BA are trei părți. Află ce arată fiecare, de ce contează sufixul și cum îl cauți corect pe FordCargo.ro.',
 lead='Codurile de piese Ford par greu de citit, dar au o structură fixă. Odată ce o cunoști, îți dai seama repede dacă două coduri sunt pentru aceeași piesă sau doar seamănă.',
 body='''
<h2>Cele trei părți</h2>
<p>Luăm ca exemplu rulmentul de presiune al ambreiajului <b>3C46 7548 BA</b>:</p>
<dl>
<dt>3C46 — prefixul</dt><dd>Arată, în general, perioada de proiectare și programul de vehicul. Pe piesele de Cargo apar des prefixe precum 3C46, 9C46, AC46 sau CC46.</dd>
<dt>7548 — baza</dt><dd>Spune ce fel de piesă este. Același număr de bază înseamnă aceeași funcție, indiferent de prefix.</dd>
<dt>BA — sufixul</dt><dd>Marchează varianta sau revizia piesei. AA este de regulă prima variantă, AB, BA etc. sunt modificări ulterioare.</dd>
</dl>
<h2>Baza arată grupa piesei</h2>
<p>Numerele de bază Ford sunt împărțite pe sisteme. Câteva grupe pe care le vezi des în catalogul nostru:</p>
<ul>
<li><b>2xxx</b> — frânare (de ex. 2L324, supapă frână de parcare)</li>
<li><b>3xxx</b> — direcție și punte față (3304, ax de direcție)</li>
<li><b>6xxx</b> — motor</li>
<li><b>7xxx</b> — ambreiaj și cutie de viteze (7550 disc de ambreiaj, 7548 rulment de presiune)</li>
<li><b>8xxx</b> — răcire</li>
<li><b>9xxx</b> — alimentare cu combustibil și emisii</li>
</ul>
<p>Pe fiecare pagină de piesă de pe FordCargo.ro scriem grupa din care face parte codul de bază.</p>
<h2>Nu tăia sufixul</h2>
<p>Două piese cu aceeași bază și sufixe diferite pot fi interschimbabile, dar pot fi și diferite: altă lungime, alt număr de caneluri, altă mufă. Caută întotdeauna codul complet. Dacă ai doar o parte din el, spune-ne asta în cerere, ca să verificăm variantele.</p>
<h2>Cum îl scrii în căutare</h2>
<p>În <a href="/cauta-piese">căutarea de pe site</a> poți scrie codul cu spații, cu cratime sau legat: <b>3C46 7548 BA</b>, <b>3C46-7548-BA</b> și <b>3C467548BA</b> găsesc aceeași piesă. Atenție la 0 și O, 1 și I: în codurile Ford litera O și litera I apar rar, deci de obicei este vorba de cifre.</p>
<p class="note">Un rezultat găsit în catalog este punctul de plecare. Compatibilitatea cu camionul tău o confirmăm în ofertă.</p>
'''),
dict(slug='coduri-t-finis-si-coduri-ford',date='2026-11-06',
 title='Coduri T, FINIS și coduri Ford: aceeași piesă, mai multe numere',
 desc='De ce aceeași piesă pentru camioane Ford apare cu un cod Ford și cu un cod T sau FINIS, și cum găsești legătura dintre ele pe FordCargo.ro.',
 lead='Pe o factură veche scrie T199352, pe piesă scrie CC46 2L324 AA. Este aceeași supapă. Situația e frecventă și creează confuzie la comandă.',
 body='''
<h2>De unde vin codurile diferite</h2>
<p>Codul Ford (de forma <b>CC46 2L324 AA</b>) este codul de proiectare marcat pe piesă. Pe lângă el, în cataloagele de distribuție, pe etichetele de ambalaj și pe facturi apar și alte numere: coduri scurte care încep cu T, ca <b>T199352</b>, sau coduri FINIS, numerice, din 7 cifre. Ele nu înlocuiesc codul Ford, ci îl însoțesc în sistemele de comandă.</p>
<h2>Cum le legăm în catalog</h2>
<p>Când avem documentată legătura dintre un cod T sau FINIS și un cod Ford, le punem pe aceeași pagină de piesă, la „Referințe asociate”. Câteva exemple din catalog:</p>
<ul>
<li><a href="/piesa/cc462l324aa/">CC46 2L324 AA</a> = T199352 — supapă releu circuit frână de parcare</li>
<li>7C46 7550 BA = T165054 — disc de ambreiaj, 430 mm</li>
<li>AC46 7K626 AA = T190733 — cilindru receptor ambreiaj</li>
</ul>
<p>Poți căuta oricare dintre ele în <a href="/cauta-piese">căutare</a>; rezultatul duce la aceeași fișă.</p>
<h2>Când nu există legătură</h2>
<p>Pentru o parte din codurile T nu avem încă un cod Ford asociat. Pagina lor arată doar codul și denumirea. Nu înseamnă că piesa nu se găsește, ci că trebuie verificată separat. Trimite-ne codul și, dacă se poate, o fotografie a piesei sau a ambalajului.</p>
<h2>Ce să nu faci</h2>
<p>Nu presupune că două coduri sunt echivalente doar pentru că au cifre asemănătoare. T199352 și T199353 pot fi piese complet diferite. Echivalența o stabilim din documente, nu din asemănarea numerelor.</p>
'''),
]

def wc(h): return len(re.sub(r'<[^>]+>',' ',h).split())

def write(path,html):
    fp=D+path+('index.html' if path.endswith('/') else '')
    os.makedirs(os.path.dirname(fp),exist_ok=True); open(fp,'w',encoding='utf-8').write(html)

json_ld_ro={}
for a in ART:
    path=f'/ghid/{a["slug"]}/'
    crumbs=[('Acasă','/'),('Ghiduri','/ghiduri'),(a['title'],path)]
    words=wc(a['body'])
    main=(crumbs_html(crumbs,'ro')+'<article class="guide">'
          f'<div class="eyebrow">GHID · {words//180+1} MIN</div><h1>{esc(a["title"])}</h1>'
          f'<p class="guide-meta">EKS LKW · <time datetime="{a["date"]}">{a["date"][8:10]}.{a["date"][5:7]}.{a["date"][:4]}</time></p>'
          f'<p class="lead">{a["lead"]}</p>{a["body"]}'
          '<p class="detail-actions"><a class="button" href="/contact">Cere ofertă</a> <a class="button secondary" href="/cauta-piese">Caută după cod</a></p>'
          '<h2>Alte ghiduri</h2><ul>'+''.join(f'<li><a href="/ghid/{b["slug"]}/">{esc(b["title"])}</a></li>' for b in ART if b is not a)+'</ul></article>')
    ld={"@context":"https://schema.org","@type":"Article","headline":a['title'],"description":a['desc'],"datePublished":a['date'],"dateModified":a['date'],
        "inLanguage":"ro","author":ORG,"publisher":{**ORG,"logo":{"@type":"ImageObject","url":SITE+"/assets/eks-lkw-logo.jpg"}},
        "mainEntityOfPage":SITE+path,"image":SITE+"/assets/parts-still-life.webp"}
    json_ld_ro[a['slug']]=ld
    write(path,page('ro',a['title']+' | EKS LKW',a['desc'],path,main,crumbs,ld=ld))

# pagina /ghiduri: lista articolelor în locul conținutului vechi
p=D+'/ghiduri.html'; h=open(p,encoding='utf-8').read()
cards=''.join(f'<article class="guide-card"><h2><a href="/ghid/{a["slug"]}/">{esc(a["title"])}</a></h2><p>{esc(a["desc"])}</p><a class="text-link" href="/ghid/{a["slug"]}/">Citește ghidul</a></article>' for a in ART)
new=('<section class="wrap page-intro"><nav class="breadcrumbs" aria-label="Fir de navigare"><a href="/">Acasă</a><span aria-hidden="true"> / </span><span aria-current="page">Ghiduri</span></nav>'
     '<h1>Ghiduri pentru piese de camioane Ford</h1><p>Explicații scurte din practica noastră de zi cu zi: cum citești un cod, ce date pregătești înainte de o cerere de ofertă și de ce aceeași piesă poate avea mai multe numere.</p></section>'
     f'<section class="wrap guide-list">{cards}</section>')
h=re.sub(r'(<main[^>]*>).*?(</main>)',lambda m:m.group(1)+new+m.group(2),h,count=1,flags=re.S)
h=re.sub(r'<title>.*?</title>','<title>Ghiduri: coduri și identificarea pieselor pentru camioane Ford | EKS LKW</title>',h,count=1,flags=re.S)
h=re.sub(r'(<meta name="description" content=")[^"]*','\\1Ghiduri practice despre codurile de piese Ford, codurile T și FINIS și datele necesare pentru a identifica piesa corectă la camioanele Ford Trucks.',h,count=1)
for k,v in (('og:title','Ghiduri: coduri și identificarea pieselor pentru camioane Ford | EKS LKW'),):
    h=re.sub(rf'(<meta property="{k}" content=")[^"]*',lambda m:m.group(1)+v,h)
open(p,'w',encoding='utf-8').write(h)
print('ghiduri:',[(a['slug'],wc(a['body'])) for a in ART])

# --- versiunea în engleză (/en/guides/...) ---
ART_EN={
'identificare-piesa-ford-cargo':dict(slug='finding-the-right-ford-cargo-part',
 title='How to find the right part for a Ford Cargo',
 desc='What to prepare before asking for a Ford Cargo part: the number on the part, where it is fitted, the VIN and the photos that help identify it.',
 lead='Two Ford Cargo trucks from the same year can have a different engine, gearbox or axle. That is why our first question on the phone is not “which model?” but “what does it say on the part?”.',
 body='''
<h2>1. Start with the old part</h2>
<p>The number on the removed part is the most reliable information. On Ford parts it usually looks like <b>7C46 7550 BA</b> (a clutch disc) or <b>CC46 2L324 AA</b> (a parking brake valve). Copy it in full, including the letters at the end, and take a clear photo of the label or stamped marking.</p>
<p>If the part carries several numbers, send all of them. One may be the Ford number, another the manufacturer's number, another a batch number. We sort them out when we check.</p>
<h2>2. Say where it is fitted</h2>
<p>For brakes, suspension and steering, the axle and side matter: front or rear, left or right. For an electrical part, photograph the connector too; the number of pins is easier to see in a photo than in a description. For hoses and pipes, a photo showing both ends helps.</p>
<h2>3. The VIN helps when the number is missing</h2>
<p>The chassis number (VIN) is in the registration document and on the plate in the cab. With it we can check the factory configuration when the part has no label left or has already been replaced by a part from another source. The VIN field in our form is optional. If you send a photo of the registration document, cover the owner's details; we only need the chassis number.</p>
<h2>4. The body has its own plate</h2>
<p>A tipper body, crane, tank or refuse compactor is not made by Ford. For those parts we need the equipment manufacturer and the serial number from the equipment plate, not the truck's VIN.</p>
<h2>5. Ask for confirmation before ordering</h2>
<p>The quote states the exact part number, the manufacturer (genuine Ford or aftermarket), the lead time and the price. If the suffix differs or there is a superseding version, we tell you before you order.</p>
<p class="note">No part number? Tell us which part you need, for which truck, and what it looks like. We start from there and ask for anything that is missing.</p>
'''),
'cod-piesa-ford-prefix-baza-sufix':dict(slug='reading-a-ford-part-number',
 title='How to read a Ford part number: prefix, base and suffix',
 desc='A Ford number like 3C46 7548 BA has three parts. What each one tells you, why the suffix matters and how to search for it on FordCargo.ro.',
 lead='Ford part numbers look hard to read, but they follow a fixed structure. Once you know it, you can quickly tell whether two numbers are the same part or just look alike.',
 body='''
<h2>The three parts</h2>
<p>Take the clutch release bearing <b>3C46 7548 BA</b> as an example:</p>
<dl>
<dt>3C46 — the prefix</dt><dd>Generally shows the design period and the vehicle programme. Cargo parts often carry prefixes such as 3C46, 9C46, AC46 or CC46.</dd>
<dt>7548 — the base</dt><dd>Tells you what kind of part it is. The same base number means the same function, whatever the prefix.</dd>
<dt>BA — the suffix</dt><dd>Marks the version or revision of the part. AA is usually the first version; AB, BA and so on are later changes.</dd>
</dl>
<h2>The base shows the part group</h2>
<p>Ford base numbers are grouped by system. Some groups you will see often in our catalogue:</p>
<ul>
<li><b>2xxx</b> — brakes (e.g. 2L324, parking brake valve)</li>
<li><b>3xxx</b> — steering and front axle (3304, drag link)</li>
<li><b>6xxx</b> — engine</li>
<li><b>7xxx</b> — clutch and gearbox (7550 clutch disc, 7548 release bearing)</li>
<li><b>8xxx</b> — cooling</li>
<li><b>9xxx</b> — fuel and emissions</li>
</ul>
<p>Every part page on FordCargo.ro states which group the base number belongs to.</p>
<h2>Don't drop the suffix</h2>
<p>Two parts with the same base and different suffixes may be interchangeable, but they may also differ: another length, another number of splines, another connector. Always search the full number. If you only have part of it, say so in your request so we can check the versions.</p>
<h2>How to type it in the search</h2>
<p>In the <a href="/en/search">site search</a> you can type the number with spaces, with hyphens or joined up: <b>3C46 7548 BA</b>, <b>3C46-7548-BA</b> and <b>3C467548BA</b> find the same part. Watch out for 0 and O, 1 and I: the letters O and I are rare in Ford numbers, so it is usually a digit.</p>
<p class="note">A catalogue result is a starting point. We confirm that it fits your truck in the quote.</p>
'''),
'coduri-t-finis-si-coduri-ford':dict(slug='t-finis-and-ford-part-numbers',
 title='T, FINIS and Ford numbers: one part, several numbers',
 desc='Why the same Ford truck part shows up with a Ford number and a T or FINIS number, and how to find the link between them on FordCargo.ro.',
 lead='An old invoice says T199352, the part itself says CC46 2L324 AA. It is the same valve. This happens a lot and causes confusion when ordering.',
 body='''
<h2>Where the different numbers come from</h2>
<p>The Ford number (such as <b>CC46 2L324 AA</b>) is the design number marked on the part. Alongside it, distribution catalogues, packaging labels and invoices use other numbers: short numbers starting with T, such as <b>T199352</b>, or numeric 7-digit FINIS numbers. They do not replace the Ford number; they accompany it in ordering systems.</p>
<h2>How we link them in the catalogue</h2>
<p>When the link between a T or FINIS number and a Ford number is documented, we show both on the same part page, under “Referințe asociate” (related references). A few examples from the catalogue:</p>
<ul>
<li><a href="/piesa/cc462l324aa/">CC46 2L324 AA</a> = T199352 — parking brake circuit relay valve</li>
<li>7C46 7550 BA = T165054 — clutch disc, 430 mm</li>
<li>AC46 7K626 AA = T190733 — clutch slave cylinder</li>
</ul>
<p>You can search any of them in the <a href="/en/search">search</a>; the result leads to the same page.</p>
<h2>When there is no link</h2>
<p>For some T numbers we do not have a matching Ford number yet. Their pages show only the number and the name. That does not mean the part cannot be found; it just has to be checked separately. Send us the number and, if possible, a photo of the part or its packaging.</p>
<h2>What not to do</h2>
<p>Don't assume two numbers are equivalent just because the digits look alike. T199352 and T199353 can be completely different parts. We establish equivalence from documents, not from similar-looking numbers.</p>
'''),
}
for a in ART:
    e=ART_EN[a['slug']]; path=f'/en/guides/{e["slug"]}/'
    crumbs=[('Home','/en/'),('Guides','/en/guides'),(e['title'],path)]
    words=wc(e['body'])
    main=(crumbs_html(crumbs,'en')+'<article class="guide">'
          f'<div class="eyebrow">GUIDE · {words//180+1} MIN</div><h1>{esc(e["title"])}</h1>'
          f'<p class="guide-meta">EKS LKW · <time datetime="{a["date"]}">{a["date"][8:10]}.{a["date"][5:7]}.{a["date"][:4]}</time></p>'
          f'<p class="lead">{e["lead"]}</p>{e["body"]}'
          '<p class="detail-actions"><a class="button" href="/en/contact">Request a quote</a> <a class="button secondary" href="/en/search">Search by part number</a></p>'
          '<h2>More guides</h2><ul>'+''.join(f'<li><a href="/en/guides/{ART_EN[b["slug"]]["slug"]}/">{esc(ART_EN[b["slug"]]["title"])}</a></li>' for b in ART if b is not a)+'</ul></article>')
    ld={"@context":"https://schema.org","@type":"Article","headline":e['title'],"description":e['desc'],"datePublished":a['date'],"dateModified":a['date'],
        "inLanguage":"en","author":ORG,"publisher":{**ORG,"logo":{"@type":"ImageObject","url":SITE+"/assets/eks-lkw-logo.jpg"}},
        "mainEntityOfPage":SITE+path,"image":SITE+"/assets/parts-still-life.webp"}
    write(path,page('en',e['title']+' | EKS LKW',e['desc'],path,main,crumbs,ld=ld,alt=('ro',f'/ghid/{a["slug"]}/')))
    # RO: legătura către EN
    rp=f'/ghid/{a["slug"]}/'
    write(rp,page('ro',a['title']+' | EKS LKW',a['desc'],rp,open(D+rp+'index.html',encoding='utf-8').read().split('<main id="main" class="wrap catalog-detail">',1)[1].rsplit('</main>',1)[0],
                  [('Acasă','/'),('Ghiduri','/ghiduri'),(a['title'],rp)],ld=json_ld_ro[a['slug']],alt=('en',path)))
print('ghiduri EN:',len(ART_EN))
