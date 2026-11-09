# ==============================================================================
#  IE350 · Hidrômetro digital com RSSF LoRa · Resumo estatístico das rodadas
# ------------------------------------------------------------------------------
#  Responsável : Lucas Chiomark Pereira Santos · RA 195111 · FEEC/UNICAMP
#  Papel       : Nível N5 · lê os arquivos brutos do framework DL/UL e calcula,
#                por rodada, PSR, RSSI e SNR (média, desvio, mínimo e máximo)
#                nos dois sentidos
#  Uso         : python analise/resumo_rodadas.py dados/brutos/<pasta>
#                (sem argumento, lê todas as subpastas de dados/brutos)
#  Saída       : tabela no terminal + dados/processados/resumo_rodadas.csv
# ==============================================================================

import csv
import statistics as st
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PASTA_BRUTOS = RAIZ / "dados" / "brutos"
ARQ_SAIDA = RAIZ / "dados" / "processados" / "resumo_rodadas.csv"

# Sensibilidade do SX1276 (datasheet RFM95) por SF, com BW = 125 kHz, em dBm.
# Usada para calcular a margem do enlace (RSSI média - sensibilidade).
SENSIBILIDADE_125K = {7: -123, 8: -126, 9: -129, 10: -132, 11: -134.5, 12: -137}

# Layout de cada linha do arquivo bruto (gerado por N2_N3_LSS_MQTT.py):
#   col 0      -> data/hora
#   col 1      -> contador da medida
#   col 2..21  -> pacote DL (20 bytes): B0 = SF, B1 = código da BW, B2 = CR, B3 = potência
#   col 22..41 -> pacote UL (20 bytes): B0 = RSSI DL, B1 = SNR DL, B2 = RSSI UL, B3 = SNR UL
#   Pacote perdido: todos os bytes do UL valem 9.
COL_DL, COL_UL = 2, 22
BW_KHZ = {1: 125, 2: 250, 3: 500}


def decodifica_rssi(byte):
    """Converte o byte de RSSI do framework para dBm (mesma regra do N5)."""
    if byte > 128:
        byte -= 256
    return byte / 2.0 - 74


def decodifica_snr(byte):
    """Converte o byte de SNR do framework para dB (mesma regra do N5)."""
    return byte / 4 - 30


def estatisticas(valores):
    """Média, desvio padrão, mínimo e máximo (None se a lista estiver vazia)."""
    if not valores:
        return dict(media=None, desvio=None, minimo=None, maximo=None)
    return dict(
        media=round(st.mean(valores), 2),
        desvio=round(st.stdev(valores), 2) if len(valores) > 1 else 0.0,
        minimo=min(valores),
        maximo=max(valores),
    )


def le_rodada(arquivo):
    """Lê um arquivo bruto e devolve o resumo da rodada em um dicionário."""
    linhas = arquivo.read_text(encoding="utf-8", errors="ignore").splitlines()[1:]
    linhas = [l.split(",") for l in linhas if l.strip()]

    enviados = len(linhas)
    rssi_dl, snr_dl, rssi_ul, snr_ul = [], [], [], []

    for partes in linhas:
        ul = [int(x) for x in partes[COL_UL:COL_UL + 20]]
        if all(b == 9 for b in ul):          # pacote perdido
            continue
        rssi_dl.append(decodifica_rssi(ul[0]))
        snr_dl.append(decodifica_snr(ul[1]))
        rssi_ul.append(decodifica_rssi(ul[2]))
        snr_ul.append(decodifica_snr(ul[3]))

    # Configuração de rádio: lida do primeiro pacote DL da rodada
    dl = [int(x) for x in linhas[0][COL_DL:COL_DL + 4]] if linhas else [0, 0, 0, 0]
    sf, bw, cr, pot = dl[0], BW_KHZ.get(dl[1], dl[1]), dl[2], dl[3]

    recebidos = len(rssi_ul)
    resumo = {
        "rodada": arquivo.stem,
        "config": f"SF{sf} BW{bw} CR4/{cr} {pot}dBm",
        "enviados": enviados,
        "recebidos": recebidos,
        "psr_%": round(100 * recebidos / enviados, 1) if enviados else 0.0,
    }
    for nome, serie in (("rssi_dl", rssi_dl), ("rssi_ul", rssi_ul),
                        ("snr_dl", snr_dl), ("snr_ul", snr_ul)):
        for k, v in estatisticas(serie).items():
            resumo[f"{nome}_{k}"] = v

    # Margem do enlace no pior sentido (menor RSSI média entre DL e UL)
    sens = SENSIBILIDADE_125K.get(sf) if bw == 125 else None
    medias = [m for m in (resumo["rssi_dl_media"], resumo["rssi_ul_media"]) if m is not None]
    resumo["margem_db"] = round(min(medias) - sens, 1) if sens and medias else None
    return resumo


def main():
    pastas = [Path(a) for a in sys.argv[1:]] or [PASTA_BRUTOS]
    arquivos = sorted(f for p in pastas for f in p.rglob("*.txt"))
    if not arquivos:
        sys.exit(f"Nenhum arquivo .txt encontrado em: {', '.join(map(str, pastas))}")

    resumos = [le_rodada(f) for f in arquivos]

    # Tabela curta no terminal
    print(f"{'Rodada':45} {'PSR%':>6} {'RSSI UL':>8} {'σ':>5} {'RSSI DL':>8} {'σ':>5} {'SNR UL':>7} {'Margem':>7}")
    for r in resumos:
        print(f"{r['rodada']:45} {r['psr_%']:6.1f} {r['rssi_ul_media']:8.1f} {r['rssi_ul_desvio']:5.2f} "
              f"{r['rssi_dl_media']:8.1f} {r['rssi_dl_desvio']:5.2f} {r['snr_ul_media']:7.2f} {r['margem_db']:7.1f}")

    # CSV completo
    ARQ_SAIDA.parent.mkdir(parents=True, exist_ok=True)
    with ARQ_SAIDA.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(resumos[0].keys()))
        w.writeheader()
        w.writerows(resumos)
    print(f"\nCSV salvo em {ARQ_SAIDA.relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
