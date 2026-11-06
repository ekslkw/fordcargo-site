# Traducere denumiri T/FINIS — FordCargo.ro (piese pentru camioane Ford)

Intrare TSV: `ID <TAB> denumire sursă <TAB> traducere RO de lucru (automată, adesea greșită)`.
Sursa este de obicei engleză de catalog Ford, cu MAJUSCULE și abrevieri (ASSY=assembly, BRKT=bracket, VLV=valve, FR/FRT=front, RR=rear, LH/RH=left/right, TRANS/TRNS=transmission, SHFT=shaft, THRST=thrust, SHM/SHIM, CYL=cylinder, HSG=housing, SPT=support, MTG=mounting, ADJ=adjuster, CONN=connector, W/=with, W/O=without, ST=side, DRIVER SIDE=partea șoferului, PASSENGER SIDE=partea pasagerului). Unele surse sunt deja în română fără diacritice (ex. „SUPAPA RELEU”) — tratează-le ca sursă română.

Ieșire TSV cu exact 3 coloane, câte o linie pentru FIECARE ID, aceeași ordine, fără antet:
`ID <TAB> denumire EN <TAB> denumire RO`

Reguli:
- Denumire de catalog scurtă și naturală, substantivul principal întâi: „Brake tube support bracket, front” / „Suport conductă frână, față”.
- EN: engleză clară, majuscule doar la început și la coduri/modele; extinde abrevierile.
- RO: română corectă cu diacritice ș ț ă â î, acord corect. Termeni: suport, conductă, furtun, garnitură, simering, rulment, bucșă, șurub, piuliță, șaibă, cablaj (wire/wiring assembly), comutator, senzor, releu, supapă, electrovalvă (solenoid valve), cilindru, carcasă, capac, cutie de viteze, ambreiaj, punte, pinion, sincron, șaibă de reglaj (shim), aripă, bară de protecție, panou, traversă, ornament, etichetă.
- Păstrează exact codurile, dimensiunile, numerele (M10, 24V, 1.5 mm etc.).
- Elimină numele de producători aftermarket; păstrează Ford/Cargo/F-MAX dacă apar.
- Dacă sursa e goală sau neinteligibilă, scrie o traducere literală prudentă; nu inventa funcții.
