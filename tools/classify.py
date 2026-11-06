"""Clasificare automată a pieselor pe grupe: cuvinte-cheie (denumire EN) + sistemul de numerotare Ford (cod de bază)."""
import re
KW=[
 ('racire', r'oil cooler|egr cooler'),
 ('motor', r'(exhaust|intake|inlet|outlet) valve|valve (spring|guide|seat|cover|stem|cotter|rotator)|valve cover|engine (mount|support|cover|block)|front cover|oil sump|oil pan|crankcase'),
 ('filtre', r'\bfilter|strainer\b'),
 ('climatizare', r'\ba/?c\b|air.?condition|condenser|evaporator|refrigerant|heater|heating|blower|climat'),
 ('turbo', r'turbo|intercooler|exhaust|muffler|silencer|tail ?pipe|catalyst|\bdpf\b|intake manifold|air intake'),
 ('franare', r'brake|air dryer|\bdrum\b|caliper|\babs\b|\bebs\b|slack adjust|air tank|air reservoir|compressor air|air compressor|four.circuit|protection valve|trailer control'),
 ('directie', r'steering|tie rod|drag link|king ?pin|track rod'),
 ('suspensie', r'shock absorb|leaf spring|(front|rear) spring|spring (front|rear)|stabili[sz]er|anti-roll|bellow|air bag|air spring|suspension|bogie|torque rod|v-?stay|u-?bolt|wheel stud|wheel nut|wheel hub|\bhub\b|wheel bearing|\brim\b'),
 ('transmisie', r'countershaft|coupling shaft|output shaft|input shaft|mainshaft|clutch|gearbox|gear box|transmission|synchro|gear ?shift|shift (fork|rod|lever)|propeller|drive ?shaft|cardan|differential|axle shaft|\bpto\b|power take|crown wheel|retarder|intarder|release bearing'),
 ('racire', r'radiator|water pump|thermostat|coolant|\bfan\b|expansion tank|cooling'),
 ('alimentare', r'return to tank|tank tube|inject|fuel|urea|adblue|\bscr\b|nox|feed pump|common rail|high pressure pump'),
 ('electric', r'pigtail|terminal kit|\bwire\b|wire assembly|wiring|cable assembly|electric wire|connector\b|bulb|lamp|light|switch|sensor|harness|wiring|relay|\bfuse|alternator|starter|battery|horn\b|\becu\b|control unit|\bamp(ere|eres|s)?\b|socket|indicator|tachograph|speedometer|instrument|cluster|antenna|radio|camera|module|solenoid'),
 ('cabina', r'door|mirror|wiper|seat\b|\bcab\b|cabin|grille|bumper|panel|spoiler|sun ?visor|emblem|\blabel|badge|\bstep\b|mudguard|fender|\bwing\b|window|glass|windscreen|windshield|handle|\block\b|latch|curtain|\broof|weatherstrip|\bmat\b|trim|console|dashboard|bunk|hinge|deflector|\bsill\b|pillar|headliner|upholster|storage|cup holder|ashtray|sticker|logo|decal|applique|instruction|warning label'),
 ('motor', r'piston|cylinder|crankshaft|camshaft|rocker|tappet|push ?rod|connecting rod|con rod|oil pump|oil pan|\bsump|timing|tensioner|idler|flywheel|engine mount|engine support|head gasket|dipstick|oil level|v-?belt|poly.?v|ribbed belt|vibration damper|crank pulley|\boil\b|liner|nhdd|ecotorq|ecoblue'),
]
KW=[(g,re.compile(r,re.I)) for g,r in KW]
def base(ref):
    t=re.sub(r'[-.]',' ',ref).replace('Y ','',1).split()
    for i,x in enumerate(t):
        if re.fullmatch(r'[A-Z0-9]{1,4}C46',x) and i+1<len(t): return t[i+1]
    return None
def ford_range(b):
    """Grupele din sistemul de numerotare Ford (cod de bază)."""
    if not b: return None
    if b[0] in 'EH': return 'cabina'
    m=re.match(r'(\d+)([A-Z]*)',b)
    if not m: return None
    dig,let=m.groups(); n=int(dig)
    if let and len(dig)<=2: n=n*1000   # ex. 6K770 -> grupa 6000, 18C553 -> 18000
    if 1000<=n<=1999: return 'suspensie'
    if 2000<=n<=2999: return 'franare'
    if 3000<=n<=3999: return 'directie'
    if 4000<=n<=4999: return 'transmisie'
    if 5000<=n<=5999: return 'alimentare' if let[:1] in ('J','H','L') else 'suspensie'
    if 6000<=n<=6999: return 'motor'
    if 7000<=n<=7999: return 'transmisie'
    if 8000<=n<=8999: return 'racire'
    if 9000<=n<=9999: return 'alimentare'
    if 10000<=n<=15999: return 'electric'
    if 16000<=n<=17999: return 'cabina'
    if 18000<=n<=19999: return 'climatizare'
    if 20000<=n<=29999: return 'cabina'
    return None
def classify(en,refs):
    for g,r in KW:
        if r.search(en): return g,'cuvant-cheie'
    for ref in refs:
        g=ford_range(base(ref))
        if g: return g,'cod-ford'
    return None,None
