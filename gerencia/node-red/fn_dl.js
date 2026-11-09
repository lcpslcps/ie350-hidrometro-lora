// Decodifica o pacote de DESCIDA (DL) publicado pelo Python N2/N3.
// Bytes: 0 = SF, 1 = código da BW, 2 = CR, 3 = potência,
//        4-5 = total de medidas da rodada, 12-13 = número da medida.
const b = msg.payload;
if (!Buffer.isBuffer(b) || b.length < 20) return null;

const BW = { 1: 125, 2: 250, 3: 500 };
const medida = b[12] * 256 + b[13];
const total  = b[4] * 256 + b[5];

// Medida 1 marca o início de uma rodada nova: zera os contadores
if (medida === 1) {
    flow.set("ul_count", 0);
    flow.set("dl_count", 0);
}
// Pacotes com medida 0 são de teste de enlace / configuração: não contam
if (medida >= 1) flow.set("dl_count", (flow.get("dl_count") || 0) + 1);

flow.set("dl_medida", medida);
flow.set("dl_total", total);

msg.payload = {
    tipo: "dl",
    t: Date.now(),
    sf: b[0], bw: BW[b[1]] || b[1], cr: b[2], pot: b[3],
    medida, total,
    nova_rodada: medida === 1
};
return msg;
