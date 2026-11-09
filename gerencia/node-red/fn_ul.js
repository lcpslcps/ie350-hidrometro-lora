// Decodifica o pacote de SUBIDA (UL) publicado pelo gateway.
// Bytes: 0 = RSSI DL, 1 = SNR DL (medidos no nó),
//        2 = RSSI UL, 3 = SNR UL (medidos no gateway), 7 = estado da rodada.
// Conversões iguais às do N5: RSSI = byte/2 - 74 (byte > 128: subtrai 256), SNR = byte/4 - 30
const b = msg.payload;
if (!Buffer.isBuffer(b) || b.length < 20) return null;

const rssi = v => (v > 128 ? v - 256 : v) / 2 - 74;
const snr  = v => v / 4 - 30;
const SENSIBILIDADE_SF12 = -137;   // dBm, SX1276 com BW 125 kHz

// Estado 6 = medida em andamento, 5 = última medida da rodada
const estado = b[7];
const valido = estado === 5 || estado === 6;

let recebidos = flow.get("ul_count") || 0;
if (valido) {
    recebidos += 1;
    flow.set("ul_count", recebidos);
}
const enviados = flow.get("dl_count") || 0;

const r_ul = rssi(b[2]);
const r_dl = rssi(b[0]);

msg.payload = {
    tipo: "ul",
    t: Date.now(),
    medida: flow.get("dl_medida") || 0,
    total:  flow.get("dl_total")  || 0,
    rssi_dl: r_dl, snr_dl: snr(b[1]),
    rssi_ul: r_ul, snr_ul: snr(b[3]),
    margem: Math.min(r_ul, r_dl) - SENSIBILIDADE_SF12,
    estado, valido, recebidos, enviados,
    psr: enviados ? Math.round(1000 * recebidos / enviados) / 10 : null
};
return msg;
