# FordCargo.ro — sursa site-ului

Site static (HTML/CSS/JS) găzduit din folderul `dist/`. Se publică doar `dist/`.

## Structură
- `data/catalog.json` — **sursa catalogului** (denumiri RO/EN, coduri, grupe). Corecturile de denumiri și categorii se fac aici.
- `data/legacy-search-data.json` — datele originale V17 (doar pentru referință / migrare).
- `tools/layout.py` — antetul, subsolul și `<head>` comune (program de lucru, CSS, Open Graph).
- `tools/build_catalog.py` — generează `dist/piesa/`, `dist/categorie/`, `dist/referinte/`, `dist/en/references/` și `dist/assets/search-data.json`.
- `tools/fix_static.py` — aplică antetul/subsolul comun pe paginile statice (acasă, contact, modele, politici).
- `tools/build_sitemaps.py` — regenerează sitemap-urile.
- `tools/classify.py` — clasificarea automată pe grupe (cuvinte-cheie + numerotarea Ford).

## Reconstruire după o modificare
```
python3 tools/apply_translations.py   # denumiri RO/EN (din data/translations/tr-final.tsv)
python3 tools/clean_codes.py          # coduri fără sufixele furnizorului
python3 tools/reclassify.py           # grupe
python3 tools/build_catalog.py        # pagini catalog + search-data.json
python3 tools/fix_static.py           # antet/subsol pe paginile statice
python3 tools/build_sitemaps.py
python3 tools/build_server.py         # .htaccess, redirect.php, _redirects
```
Pentru o corectură de denumire: modifică linia din `data/translations/tr-final.tsv` și rulează comenzile de mai sus.

## Publicare (Zooku)
Se încarcă conținutul folderului `dist/` în rădăcina site-ului (public_html al domeniului fordcargo.ro), inclusiv fișierul ascuns `.htaccess`. PHP 7.4 sau mai nou.
