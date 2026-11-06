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
