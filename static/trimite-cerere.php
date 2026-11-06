<?php
/*
 * FordCargo.ro — trimiterea cererii de ofertă pe e-mail (formularul /contact).
 * Destinatar fix: office@eurokolben.ro. Expeditor: noreply@fordcargo.ro (domeniul găzduit pe acest cont cPanel).
 * Adresa vizitatorului apare doar ca Reply-To. Conținutul formularului NU se salvează pe server;
 * pentru limitarea abuzurilor se păstrează temporar doar o amprentă (hash) a IP-ului, în afara public_html.
 */
declare(strict_types=1);

const TO_EMAIL   = 'office@eurokolben.ro';
const FROM_EMAIL = 'noreply@fordcargo.ro';
const FROM_NAME  = 'FordCargo.ro';
const ALLOWED_HOSTS = ['fordcargo.ro', 'www.fordcargo.ro'];
const MAX_PER_IP_15MIN = 5;
const MAX_PER_DAY = 150;
const MIN_FILL_SECONDS = 3;

header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store');
header('X-Content-Type-Options: nosniff');

function out(int $code, array $body): void {
    http_response_code($code);
    echo json_encode($body, JSON_UNESCAPED_UNICODE);
    exit;
}

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    out(405, ['ok' => false, 'error' => 'method']);
}

// Doar cereri din pagina site-ului (Origin sau Referer de pe fordcargo.ro)
$src = $_SERVER['HTTP_ORIGIN'] ?? ($_SERVER['HTTP_REFERER'] ?? '');
$host = strtolower((string)parse_url($src, PHP_URL_HOST));
if (!in_array($host, ALLOWED_HOSTS, true)) {
    out(403, ['ok' => false, 'error' => 'origin']);
}

$raw = file_get_contents('php://input', false, null, 0, 20000);
$in = json_decode((string)$raw, true);
if (!is_array($in)) {
    out(400, ['ok' => false, 'error' => 'format']);
}

function field(array $in, string $k, int $max): string {
    $v = isset($in[$k]) && is_string($in[$k]) ? $in[$k] : '';
    $v = preg_replace('/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/u', '', $v) ?? '';
    $v = trim($v);
    return mb_substr($v, 0, $max);
}
function oneline(string $v): string {
    return trim(preg_replace('/[\r\n]+/', ' ', $v) ?? '');
}

// Capcane pentru boți: câmp ascuns completat sau formular trimis prea repede
if (field($in, 'website', 200) !== '') {
    out(200, ['ok' => true]); // răspuns neutru, fără trimitere
}
$t = isset($in['t']) && is_numeric($in['t']) ? (int)$in['t'] : 0;
if ($t <= 0 || (time() * 1000 - $t) < MIN_FILL_SECONDS * 1000) {
    out(400, ['ok' => false, 'error' => 'timing']);
}

$prenume = oneline(field($in, 'prenume', 80));
$nume    = oneline(field($in, 'nume', 80));
$telefon = oneline(field($in, 'telefon', 30));
$email   = oneline(field($in, 'email', 160));
$vin     = oneline(field($in, 'vin', 30));
$piesa   = field($in, 'piesa', 2500);
$consent = !empty($in['consent']);

if ($prenume === '' || $telefon === '' || $piesa === '' || !$consent) {
    out(422, ['ok' => false, 'error' => 'required']);
}
if (!preg_match('/^[0-9+()\s.\/-]{6,30}$/', $telefon)) {
    out(422, ['ok' => false, 'error' => 'phone']);
}
if ($email !== '' && !filter_var($email, FILTER_VALIDATE_EMAIL)) {
    out(422, ['ok' => false, 'error' => 'email']);
}

// Limitare: pe IP (hash) și total pe zi, stocare în afara public_html
$stateDir = dirname(__DIR__) . '/fordcargo-form-state';
if (!is_dir($stateDir) && !@mkdir($stateDir, 0700, true)) {
    out(500, ['ok' => false, 'error' => 'state']);
}
$stateFile = $stateDir . '/limits.json';
$fh = @fopen($stateFile, 'c+');
if (!$fh || !flock($fh, LOCK_EX)) {
    out(500, ['ok' => false, 'error' => 'state']);
}
$state = json_decode((string)stream_get_contents($fh), true) ?: [];
$now = time();
$day = date('Y-m-d');
$ipHash = hash('sha256', ($_SERVER['REMOTE_ADDR'] ?? '') . '|' . __FILE__);
$state['ip'] = array_filter($state['ip'] ?? [], fn($ts) => is_array($ts) && $ts && max($ts) > $now - 900);
foreach ($state['ip'] as $k => $ts) { $state['ip'][$k] = array_values(array_filter($ts, fn($x) => $x > $now - 900)); }
$mine = $state['ip'][$ipHash] ?? [];
if (($state['day'] ?? '') !== $day) { $state['day'] = $day; $state['count'] = 0; }
if (count($mine) >= MAX_PER_IP_15MIN || ($state['count'] ?? 0) >= MAX_PER_DAY) {
    flock($fh, LOCK_UN); fclose($fh);
    out(429, ['ok' => false, 'error' => 'limit']);
}

// Mesajul
$numeComplet = trim($prenume . ' ' . $nume);
$subject = 'Cerere ofertă fordcargo.ro — ' . $numeComplet;
$body = "Cerere nouă de ofertă de pe fordcargo.ro\n"
      . "----------------------------------------\n"
      . "Nume: {$numeComplet}\n"
      . "Telefon: {$telefon}\n"
      . 'E-mail: ' . ($email !== '' ? $email : '-') . "\n"
      . 'VIN: ' . ($vin !== '' ? $vin : '-') . "\n\n"
      . "Piesa dorită / descriere:\n{$piesa}\n\n"
      . "----------------------------------------\n"
      . 'Trimis la: ' . date('d.m.Y H:i') . "\n"
      . "Clientul a confirmat Politica de Confidențialitate.\n";

$headers = [
    'From: ' . '=?UTF-8?B?' . base64_encode(FROM_NAME) . '?= <' . FROM_EMAIL . '>',
    'MIME-Version: 1.0',
    'Content-Type: text/plain; charset=UTF-8',
    'Content-Transfer-Encoding: 8bit',
    'X-Mailer: fordcargo-form',
];
if ($email !== '') {
    $headers[] = 'Reply-To: ' . $email;
}
$sent = @mail(
    TO_EMAIL,
    '=?UTF-8?B?' . base64_encode($subject) . '?=',
    $body,
    implode("\r\n", $headers),
    '-f' . FROM_EMAIL
);

if ($sent) {
    $mine[] = $now;
    $state['ip'][$ipHash] = $mine;
    $state['count'] = ($state['count'] ?? 0) + 1;
}
ftruncate($fh, 0); rewind($fh);
fwrite($fh, json_encode($state));
flock($fh, LOCK_UN); fclose($fh);

if (!$sent) {
    out(502, ['ok' => false, 'error' => 'mail']);
}
out(200, ['ok' => true]);
