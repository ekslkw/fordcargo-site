"""Regenerează sitemap-urile din paginile indexabile din dist/ (canonical + robots index)."""
import os,re,datetime
D='dist'; S='https://fordcargo.ro'; today=datetime.date.today().isoformat()
groups={'pagini':[],'categorii':[],'piese':[]}
for dp,_,fs in os.walk(D):
    for f in fs:
        if not f.endswith('.html'): continue
        h=open(os.path.join(dp,f),encoding='utf-8').read(2600)
        if 'noindex' in h: continue
        m=re.search(r'rel="canonical" href="(https://fordcargo\.ro[^"]*)"',h)
        if not m: continue
        u=m.group(1); path=u[len(S):]
        k='piese' if path.startswith('/piesa/') else 'categorii' if path.startswith('/categorie/') else 'pagini'
        groups[k].append(u)
for k,urls in groups.items():
    body=''.join(f'<url><loc>{u}</loc><lastmod>{today}</lastmod></url>' for u in sorted(set(urls)))
    open(f'{D}/sitemap-{k}.xml','w').write(f"<?xml version='1.0' encoding='utf-8'?>\n<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">{body}</urlset>")
    print(k,len(set(urls)))
idx=''.join(f'<sitemap><loc>{S}/sitemap-{k}.xml</loc><lastmod>{today}</lastmod></sitemap>' for k in groups)
open(f'{D}/sitemap.xml','w').write(f"<?xml version='1.0' encoding='utf-8'?>\n<sitemapindex xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">{idx}</sitemapindex>")
