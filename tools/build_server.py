import os
"""Generează configurația serverului:
- dist/.htaccess  (Apache / Zooku): HTTPS, fără www, URL-uri fără .html, antete de securitate, cache, 404, redirecționări
- dist/redirect.php (tabelul de redirecționări pentru adresele vechi, servit doar când pagina nu există)
- dist/_redirects (același tabel în format Netlify/Cloudflare, pentru alte gazde)"""
import json
D='dist'
STATIC=[('/magazin','/catalog'),('/magazin.html','/catalog'),('/despre-noi.html','/despre-noi'),('/contact.html','/contact'),('/cauta-piese.html','/cauta-piese')]
rules=json.load(open('data/redirects-all.json'))
CSP=("default-src 'self'; script-src 'self'; script-src-elem 'self' 'unsafe-inline'; script-src-attr 'none'; style-src 'self' 'unsafe-inline'; "
     "img-src 'self' data:; font-src 'self'; connect-src 'self'; frame-src https://www.google.com https://maps.google.com; object-src 'none'; "
     "base-uri 'none'; form-action 'self'; upgrade-insecure-requests; frame-ancestors 'none'")
ZOOKU='''
# BEGIN cPanel-generated php ini directives, do not edit
<IfModule php8_module>
   php_value error_log "/home/u43916ford/logs/php.error.log"
   php_flag log_errors On
</IfModule>
<IfModule lsapi_module>
   php_value error_log "/home/u43916ford/logs/php.error.log"
   php_flag log_errors On
</IfModule>
# END cPanel-generated php ini directives, do not edit
'''
ESC=lambda a:a.lstrip('/').replace('.','\\.')
ht=f"""# FordCargo.ro — configurație Apache (Zooku). Generat de tools/build_server.py
Options -Indexes -MultiViews
DirectoryIndex index.html
AddDefaultCharset utf-8
ErrorDocument 404 /404.html

<IfModule mod_rewrite.c>
RewriteEngine On
# validarea certificatului SSL (AutoSSL / Let's Encrypt) rămâne pe HTTP, fără redirecționări
RewriteRule ^\\.well-known/ - [L]
# HTTPS și domeniu fără www
RewriteCond %{{HTTPS}} !=on [OR]
RewriteCond %{{HTTP_HOST}} ^www\\. [NC]
RewriteRule ^ https://fordcargo.ro%{{REQUEST_URI}} [R=301,L]
# datele căutării se descarcă doar din paginile site-ului (nu direct)
RewriteCond %{{HTTP_REFERER}} !^https://(www\\.)?fordcargo\\.ro/ [NC]
RewriteRule ^assets/sd-[0-9a-f]+\\.txt$ - [F,L]
# redirecționări fixe
""" + ''.join(f"RewriteRule ^{ESC(a)}$ {b} [R=301,L]\n" for a,b in STATIC) + """# /pagina.html -> /pagina (doar la cererea directă a clientului)
RewriteCond %{THE_REQUEST} \\s/([^\\s?]+)\\.html[\\s?] [NC]
RewriteCond %{REQUEST_URI} !^/404\\.html$
RewriteRule ^ /%1 [R=301,L]
# /pagina -> pagina.html
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteCond %{DOCUMENT_ROOT}/$1.html -f
RewriteRule ^(.+?)/?$ $1.html [L]
# adrese vechi (catalog V17) -> redirect.php
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule ^ /redirect.php [L]
</IfModule>

<IfModule mod_headers.c>
Header always set Strict-Transport-Security "max-age=31536000"
Header always set X-Content-Type-Options "nosniff"
Header always set X-Frame-Options "DENY"
Header always set Referrer-Policy "no-referrer"
Header always set Permissions-Policy "camera=(), microphone=(), geolocation=()"
Header always set Content-Security-Policy "__CSP__"
<FilesMatch "\\.(css|js|svg|png|jpg|jpeg|webp|ico)$">
Header set Cache-Control "public, max-age=2592000"
</FilesMatch>
<FilesMatch "\\.(html|json|xml)$">
Header set Cache-Control "public, max-age=600"
</FilesMatch>
</IfModule>

<IfModule mod_deflate.c>
AddOutputFilterByType DEFLATE text/html text/css application/javascript application/json image/svg+xml application/xml
</IfModule>

# fișiere interne
<FilesMatch "^(_headers|_redirects)$">
Require all denied
</FilesMatch>
""".replace("__CSP__",CSP)
open(f'{D}/.htaccess','w').write(ht+ZOOKU)
php_map=',\n'.join(f"'{a}'=>'{b}'" for a,b in sorted(rules.items()))
php=f"""<?php
// Redirecționări 301 pentru adresele vechi ale catalogului. Generat de tools/build_server.py
$map = [
{php_map}
];
$p = parse_url($_SERVER['REQUEST_URI'] ?? '/', PHP_URL_PATH) ?: '/';
$p = rawurldecode($p);
$k = rtrim($p, '/') . '/';
$t = $map[$k] ?? $map[$p] ?? null;
if ($t !== null) {{ header('Location: https://fordcargo.ro' . $t, true, 301); exit; }}
http_response_code(404);
header('Content-Type: text/html; charset=utf-8');
readfile(__DIR__ . '/404.html');
"""
open(f'{D}/redirect.php','w').write(php)
lines=[f'{a} {b} 301' for a,b in STATIC]+[f'{a} {b} 301' for a,b in sorted(rules.items())]
open(f'{D}/_redirects','w').write('\n'.join(lines)+'\n')
print('reguli',len(rules)+len(STATIC))

import shutil
shutil.copy('static/trimite-cerere.php', f'{D}/trimite-cerere.php')
print('trimite-cerere.php copiat')
import glob
for f in ['static/robots.txt','static/llms.txt']+glob.glob('static/fordcargoro*.txt'):
    shutil.copy(f, f'{D}/'+os.path.basename(f))
print('robots.txt, llms.txt, cheie IndexNow copiate')

# --- datele căutării: nu se publică JSON-ul brut (fișier codificat + acces doar din paginile site-ului)
import hashlib,random,re as _re
src=f'{D}/assets/search-data.json'
if os.path.exists(src):
    txt=open(src,encoding='utf-8').read()
    chars=[chr(c) for c in range(33,127)]
    perm=chars[:]; random.Random(1990).shuffle(perm)
    enc=txt.translate(str.maketrans(''.join(chars),''.join(perm)))
    h=hashlib.sha256(enc.encode()).hexdigest()[:10]
    for f in os.listdir(f'{D}/assets'):
        if f.startswith('sd-') and f.endswith('.txt'): os.remove(f'{D}/assets/{f}')
    open(f'{D}/assets/sd-{h}.txt','w',encoding='utf-8').write(enc)
    os.remove(src)
    js=f'{D}/unified-search.js'; j=open(js,encoding='utf-8').read()
    dec=("(t=>{const A='"+''.join(chars).replace('\\','\\\\').replace("'","\\'")+"',B='"+''.join(perm).replace('\\','\\\\').replace("'","\\'")+"';const m={};for(let i=0;i<B.length;i++)m[B[i]]=A[i];"
         "let o='';for(const c of t)o+=m[c]||c;return JSON.parse(o)})")
    j=_re.sub(r"fetch\('/assets/(?:search-data\.json\?v=\d+|sd-[0-9a-f]+\.txt)'\)\.then\(r=>\{if\(!r\.ok\)throw Error\('load'\);return (?:r\.json\(\)|r\.text\(\)\.then\(.*?\))\}",
               lambda m:f"fetch('/assets/sd-{h}.txt').then(r=>{{if(!r.ok)throw Error('load');return r.text().then({dec})}}",j,count=1,flags=_re.S)
    open(js,'w',encoding='utf-8').write(j)
    print('date căutare codificate:',f'sd-{h}.txt')
