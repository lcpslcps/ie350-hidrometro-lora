# ==============================================================================
#  IE350 · Hidrômetro digital com RSSF LoRa · Gráficos da campanha de 09/11
# ------------------------------------------------------------------------------
#  Responsável : Lucas Chiomark Pereira Santos · RA 195111 · FEEC/UNICAMP
#  Papel       : Nível N5 · gera as figuras de resultado a partir dos .txt brutos
#  Uso         : python analise/graficos.py
#  Saída       : docs/figuras/resultados/*.png
# ==============================================================================

import statistics as st
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

RAIZ = Path(__file__).resolve().parent.parent
PREDIO = RAIZ / "dados" / "brutos" / "predio_2026-11-09"
APTO = RAIZ / "dados" / "brutos" / "apartamento_2026-11-09"
SAIDA = RAIZ / "docs" / "figuras" / "resultados"

# Paleta (slots 1 e 2 da paleta categórica validada) e tinta de texto
AZUL, LARANJA, CINZA = "#2a78d6", "#eb6834", "#8a8984"
TXT, TXT2, GRADE, FUNDO = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 10, "axes.edgecolor": GRADE,
    "axes.labelcolor": TXT2, "xtick.color": TXT2, "ytick.color": TXT2,
    "axes.titlecolor": TXT, "axes.titlesize": 11, "axes.titleweight": "bold",
    "axes.grid": True, "grid.color": GRADE, "grid.linewidth": 0.6,
    "axes.spines.top": False, "axes.spines.right": False,
    "figure.facecolor": FUNDO, "axes.facecolor": FUNDO, "savefig.dpi": 160,
})


def rssi(byte):
    """Byte de RSSI do framework → dBm (mesma regra do N5)."""
    return (byte - 256 if byte > 128 else byte) / 2 - 74


def le(arquivo):
    """Lista de (medida, RSSI UL, RSSI DL) só com os pacotes recebidos."""
    pts = []
    for linha in arquivo.read_text(encoding="utf-8").splitlines()[1:]:
        p = [x.strip() for x in linha.split(",")]
        ul = [int(x) for x in p[22:42]]
        if all(b == 9 for b in ul):
            continue
        pts.append((int(p[1]), rssi(ul[2]), rssi(ul[0])))
    return pts


def acha(pasta, prefixo):
    return next(pasta.glob(f"{prefixo}_*.txt"))


def media_uldl(pts):
    return [(m, (u + d) / 2) for m, u, d in pts]


def salva(fig, nome):
    SAIDA.mkdir(parents=True, exist_ok=True)
    fig.savefig(SAIDA / nome, bbox_inches="tight")
    plt.close(fig)
    print("ok", nome)


# ---------------------------------------------------------------------------
# 1. Elevador parado × em movimento (H1)
# ---------------------------------------------------------------------------
def fig_parado_vs_mov():
    fig, eixos = plt.subplots(1, 2, figsize=(11, 3.8), sharey=True)
    casos = [("Nó no térreo ↔ gateway no 2º andar", "R_A0_", "R_A1_"),
             ("Nó na casa de máquinas ↔ gateway no 2º andar", "R_B0_", "R_B1_")]
    for ax, (titulo, p0, p1) in zip(eixos, casos):
        for pref, cor, rot in [(p0, AZUL, "parado"), (p1, LARANJA, "em movimento")]:
            serie = media_uldl(le(acha(PREDIO, pref.rstrip("_"))))
            x, y = zip(*serie)
            s = st.stdev(y)
            ax.plot(x, y, color=cor, lw=2, marker="o", ms=3, label=f"{rot} (σ = {s:.1f} dB)")
        ax.set_title(titulo, loc="left")
        ax.set_xlabel("medida")
        ax.legend(frameon=False, loc="lower right", fontsize=9)
    eixos[0].set_ylabel("RSSI (dBm, média UL/DL)")
    fig.suptitle("Com o elevador andando, a média muda pouco e a variação cresce", x=0.01, y=1.03, ha="left",
                 fontsize=12, fontweight="bold", color=TXT)
    salva(fig, "parado_vs_movimento.png")


# ---------------------------------------------------------------------------
# 2. Desvio padrão por rodada
# ---------------------------------------------------------------------------
def fig_sigma():
    rodadas = [("Referência 1 m", APTO, "R_R0"), ("Térreo parado (A0)", PREDIO, "R_A0"),
               ("Térreo em mov. (A1)", PREDIO, "R_A1"), ("Casa máq. parado (B0)", PREDIO, "R_B0"),
               ("Casa máq. em mov. (B1)", PREDIO, "R_B1")]
    nomes, sig = [], []
    for nome, pasta, pref in rodadas:
        y = [v for _, v in media_uldl(le(acha(pasta, pref)))]
        nomes.append(nome); sig.append(st.stdev(y))
    # Cabine: só o trecho dentro do elevador (medidas 7 a 33)
    c = [v for m, v in media_uldl(le(acha(PREDIO, "R_C"))) if 7 <= m <= 33]
    nomes.append("Nó na cabine (C)"); sig.append(st.stdev(c))
    cores = [CINZA, AZUL, LARANJA, AZUL, LARANJA, LARANJA]
    fig, ax = plt.subplots(figsize=(8, 3.6))
    y = range(len(nomes))[::-1]
    ax.barh(list(y), sig, color=cores, height=0.6)
    for yi, s in zip(y, sig):
        ax.text(s + 0.08, yi, f"{s:.1f} dB", va="center", color=TXT, fontsize=9)
    ax.set_yticks(list(y), nomes)
    ax.set_xlabel("σ da RSSI (dB)")
    ax.set_xlim(0, max(sig) * 1.2)
    ax.set_title("Desvio padrão da RSSI (cinza: referência · azul: parado · laranja: em movimento)", loc="left", fontsize=10)
    ax.grid(axis="y", visible=False)
    salva(fig, "sigma_por_rodada.png")


# ---------------------------------------------------------------------------
# 3. Posição da cabine parada (A2) - trechos identificados no vídeo
# ---------------------------------------------------------------------------
def fig_cabine_andar():
    serie = dict(media_uldl(le(acha(PREDIO, "R_A2"))))
    trechos = [("2º\n(início)", 1, 11), ("Térreo", 13, 17), ("1º", 18, 22), ("2º", 23, 27),
               ("3º", 28, 31), ("4º", 32, 38), ("2º\n(volta)", 43, 48)]
    base = st.mean(v for _, v in media_uldl(le(acha(PREDIO, "R_A0"))))
    nomes = [t[0] for t in trechos]
    vals = [st.mean(serie[m] for m in range(a, b + 1) if m in serie) for _, a, b in trechos]
    fig, ax = plt.subplots(figsize=(8, 3.6))
    ax.bar(nomes, [v - base for v in vals], color=[AZUL if v >= base else LARANJA for v in vals], width=0.6)
    for i, v in enumerate(vals):
        d = v - base
        ax.text(i, d + (0.4 if d >= 0 else -1.2), f"{d:+.1f}", ha="center", color=TXT, fontsize=9)
    ax.axhline(0, color=TXT2, lw=1)
    ax.set_ylim(min(v - base for v in vals) - 2.5, max(v - base for v in vals) + 2)
    ax.set_ylabel("diferença p/ linha de base (dB)")
    ax.set_title(f"Nó fixo no térreo: cabine parada em cada andar (base A0 = {base:.1f} dBm)", loc="left")
    ax.grid(axis="x", visible=False)
    salva(fig, "cabine_parada_por_andar.png")


# ---------------------------------------------------------------------------
# 4. Fonte do nó: tomada × power bank
# ---------------------------------------------------------------------------
def fig_fonte():
    pares = [("Térreo", "R_A0", "R_A0pb"), ("Casa de máquinas", "R_B0", "R_B0pb")]
    fig, ax = plt.subplots(figsize=(7, 3.4))
    for i, (nome, t, pb) in enumerate(pares):
        vt = st.mean(u for _, u, _ in le(acha(PREDIO, t)))
        vp = st.mean(u for _, u, _ in le(acha(PREDIO, pb)))
        ax.plot([vp, vt], [i, i], color=GRADE, lw=6, solid_capstyle="round", zorder=1)
        ax.scatter([vt], [i], s=90, color=AZUL, zorder=2, label="tomada" if i == 0 else None)
        ax.scatter([vp], [i], s=90, color=LARANJA, zorder=2, label="power bank" if i == 0 else None)
        ax.text(vt, i + 0.22, f"{vt:.1f}", ha="center", color=TXT, fontsize=9)
        ax.text(vp, i + 0.22, f"{vp:.1f}", ha="center", color=TXT, fontsize=9)
        ax.text((vt + vp) / 2, i - 0.28, f"{vt - vp:.0f} dB", ha="center", color=TXT2, fontsize=9)
    ax.set_yticks(range(len(pares)), [p[0] for p in pares])
    ax.set_ylim(-0.7, len(pares) - 0.4)
    ax.set_xlabel("RSSI UL média (dBm)")
    ax.legend(frameon=False, loc="lower left", ncol=2)
    ax.set_title("Mesma posição: a fonte do nó mudou a RSSI em 17 a 29 dB", loc="left")
    ax.grid(axis="y", visible=False)
    salva(fig, "fonte_tomada_vs_powerbank.png")


# ---------------------------------------------------------------------------
# 5. Nó dentro da cabine: trajeto completo (C)
# ---------------------------------------------------------------------------
def fig_cabine_trajeto():
    pts = [p for p in le(acha(PREDIO, "R_C")) if p[0] <= 43]
    m, u, d = zip(*pts)
    fig, ax = plt.subplots(figsize=(10, 3.8))
    for a, b, rot in [(1, 6, "levando o nó\naté o elevador"), (7, 33, "nó dentro da cabine"),
                      (34, 43, "voltando ao\napartamento")]:
        ax.axvspan(a - 0.5, b + 0.5, color=GRADE if rot.startswith("nó") else "#f1f0ec", zorder=0)
        ax.text((a + b) / 2, -18, rot, ha="center", va="top", color=TXT2, fontsize=8.5)
    ax.plot(m, u, color=AZUL, lw=2, marker="o", ms=3, label="UL")
    ax.plot(m, d, color=LARANJA, lw=2, marker="o", ms=3, label="DL")
    ax.set_ylim(-95, -15)
    ax.set_xlabel("medida")
    ax.set_ylabel("RSSI (dBm)")
    ax.legend(frameon=False, loc="lower left", ncol=2)
    ax.set_title("Nó dentro da cabine (trajeto 2 → T → 1 → 3 → 4 → 1 → T), PSR 100% no trecho", loc="left")
    salva(fig, "cabine_trajeto.png")


if __name__ == "__main__":
    fig_parado_vs_mov()
    fig_sigma()
    fig_cabine_andar()
    fig_fonte()
    fig_cabine_trajeto()
