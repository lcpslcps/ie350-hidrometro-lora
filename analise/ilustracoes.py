# ==============================================================================
#  IE350 · Hidrômetro digital com RSSF LoRa · Ilustrações dos ensaios
# ------------------------------------------------------------------------------
#  Responsável : Lucas Chiomark Pereira Santos · RA 195111 · FEEC/UNICAMP
#  Papel       : desenha o corte do prédio e as plantas esquemáticas com as
#                posições usadas na campanha de 09/11/2026 (sem escala)
#  Uso         : python analise/ilustracoes.py  ->  docs/figuras/*.png
# ==============================================================================

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Polygon

SAIDA = Path(__file__).resolve().parent.parent / "docs" / "figuras"
AZUL, LARANJA, VERDE, CINZA = "#2a78d6", "#eb6834", "#1baf7a", "#8a8984"
TXT, TXT2, PAREDE, PISO, FUNDO = "#0b0b0b", "#52514e", "#444441", "#f4f3ef", "#fcfcfb"
plt.rcParams.update({"font.family": "DejaVu Sans", "figure.facecolor": FUNDO, "savefig.dpi": 170})


def gw(ax, x, y, rot="GW", dx=0, dy=-.3, ha="center", va="top"):
    ax.add_patch(Polygon([[x - .28, y], [x + .28, y], [x, y + .5]], fc=LARANJA, ec="white", zorder=5))
    ax.text(x + dx, y + dy, rot, ha=ha, va=va, fontsize=8, color=LARANJA, fontweight="bold")


def no(ax, x, y, rot, cor=AZUL, lado="left"):
    ax.plot(x, y, "o", ms=11, color=cor, mec="white", mew=1.5, zorder=5)
    dx = -.35 if lado == "left" else .35
    ax.text(x + dx, y, rot, ha="right" if lado == "left" else "left", va="center",
            fontsize=8, color=cor, fontweight="bold")


def corte():
    fig, ax = plt.subplots(figsize=(10, 7.5))
    ax.set_xlim(0, 16); ax.set_ylim(-.8, 9.6); ax.axis("off")
    andares = ["Térreo", "1º", "2º", "3º", "4º"]
    H = 1.5
    for i, a in enumerate(andares):
        ax.add_patch(Rectangle((2, i * H), 10, H, fc=PISO if i else "#eeeae0", ec=PAREDE, lw=1))
        ax.text(1.8, i * H + H / 2, a, ha="right", va="center", fontsize=10, color=TXT)
    # cobertura e casa de máquinas
    ax.add_patch(Rectangle((5, 5 * H), 3.2, 1.1, fc="#e4e3df", ec=PAREDE, lw=1.4))
    ax.text(6.6, 5 * H + .8, "casa de máquinas", ha="center", fontsize=8.5, color=TXT2)
    ax.plot([0.5, 15.5], [0, 0], color="#6b5a3a", lw=2)
    # poço do elevador
    ax.add_patch(Rectangle((6, 0), 1.3, 5 * H, fc="#dcdad3", ec=PAREDE, hatch="////", lw=.8))
    ax.add_patch(Rectangle((6.1, 2 * H + .15), 1.1, 1.0, fc=CINZA, ec=TXT, lw=1, zorder=3))
    ax.text(6.65, 2 * H + .65, "cabine", ha="center", va="center", fontsize=7, color="white", zorder=4)
    ax.annotate("", xy=(7.65, 5.6), xytext=(7.65, .6), arrowprops=dict(arrowstyle="<->", color=TXT2))
    ax.text(7.8, 1.0, "percurso\nda cabine", fontsize=8, color=TXT2, va="center")
    # apartamento 2º andar (gateway fixo)
    ax.add_patch(Rectangle((9, 2 * H), 3, H, fc="#fdf0e8", ec=LARANJA, lw=1.2, ls="--"))
    ax.text(10.5, 2 * H + 1.25, "apartamento (Wi-Fi)", ha="center", fontsize=7.5, color=LARANJA)
    gw(ax, 9.6, 2 * H + .35, "GW fixo", dy=-.6)
    # posições do nó
    no(ax, 5.3, .55, "A0 · A1 · A2\nnó no hall do térreo")
    no(ax, 4.6, 5 * H + .3, "")
    ax.text(4.25, 5 * H + .3, "B0 · B1: nó no acesso\nà casa de máquinas", ha="right", va="center", fontsize=8, color=AZUL, fontweight="bold")
    no(ax, 6.65, 2 * H - .55, "", cor=VERDE)
    ax.text(5.9, 2 * H - .55, "C · nó dentro\nda cabine", ha="right", va="center", fontsize=8, color=VERDE, fontweight="bold")
    no(ax, 11.4, 2 * H + .35, "")
    ax.text(12.3, 2 * H + .35, "R0: nó a 1 m do GW\nL: lavanderia, 9 m\ne 3 paredes", ha="left", va="center",
            fontsize=8, color=AZUL, fontweight="bold")
    # enlaces
    for (x, y) in [(5.3, .55), (4.6, 5 * H + .3)]:
        ax.plot([x, 9.6], [y, 2 * H + .6], ls=":", color=TXT2, lw=1)
    ax.text(14.2, 8.9, "Gateway sempre no 2º andar.\nO nó muda de lugar; pela\nreciprocidade do canal, o\nenlace equivale ao inverso.",
            fontsize=8.5, color=TXT2, va="top", ha="center",
            bbox=dict(boxstyle="round,pad=.5", fc="white", ec="#e4e3df"))
    ax.text(.5, -.6, "Corte esquemático, sem escala · térreo + 4 andares · 903 MHz, SF12, BW 125 kHz, 20 dBm",
            fontsize=8, color=TXT2)
    ax.set_title("Posições usadas na campanha de 09/11/2026", loc="left", fontsize=12, fontweight="bold", color=TXT)
    fig.savefig(SAIDA / "corte_predio_ensaios.png", bbox_inches="tight"); plt.close(fig)


def planta(ax, titulo):
    ax.set_xlim(0, 10); ax.set_ylim(0, 7); ax.set_aspect("equal"); ax.axis("off")
    ax.set_title(titulo, loc="left", fontsize=10.5, fontweight="bold", color=TXT)
    ax.add_patch(Rectangle((.2, .2), 9.6, 6.6, fc=PISO, ec=PAREDE, lw=1.6))
    # poço do elevador e escada (comuns aos dois andares)
    ax.add_patch(Rectangle((.2, 4.4), 2.2, 2.4, fc="#dcdad3", ec=PAREDE, hatch="////", lw=.8))
    ax.text(1.3, 5.6, "poço do\nelevador", ha="center", va="center", fontsize=8, color=TXT,
            bbox=dict(boxstyle="round,pad=.2", fc="white", ec="none"))
    ax.plot([2.45, 2.45], [4.7, 6.4], color=AZUL, lw=3)
    ax.text(2.6, 6.55, "porta", fontsize=7, color=TXT2)
    ax.add_patch(Rectangle((7.4, 4.4), 2.4, 2.4, fc="#ebe9e3", ec=PAREDE, lw=.8))
    for k in range(6):
        ax.plot([7.4, 9.8], [4.6 + k * .35] * 2, color="#c9c7c0", lw=.8)
    ax.text(8.6, 3.9, "escada", ha="center", fontsize=8, color=TXT2)
    ax.text(5, 5.6, "hall", ha="center", fontsize=9, color=TXT2)


def plantas():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(12, 4.3))
    planta(a1, "Térreo: nó das rodadas A0, A1 e A2")
    a1.add_patch(Rectangle((3.4, 2.3), 1.2, .8, fc="white", ec=TXT2, lw=.8))
    a1.text(4.0, 2.0, "mesa", ha="center", va="top", fontsize=7, color=TXT2)
    a1.plot(4.0, 2.7, "o", ms=11, color=AZUL, mec="white", mew=1.5, zorder=5)
    a1.text(4.9, 2.7, "nó (tomada)\n~3 m da porta", ha="left", va="center", fontsize=8, color=AZUL, fontweight="bold")
    a1.add_patch(Rectangle((.2, .2), 3, 1.6, fc="#eeeae0", ec=PAREDE, lw=.8))
    a1.text(1.7, 1.0, "corredor /\nárea técnica", ha="center", va="center", fontsize=7.5, color=TXT2)
    planta(a2, "2º andar: gateway fixo (todas as rodadas)")
    a2.add_patch(Rectangle((3.2, .2), 4.0, 2.4, fc="#fdf0e8", ec=LARANJA, lw=1.2, ls="--"))
    a2.text(5.2, .5, "apartamento 22", ha="center", fontsize=8, color=LARANJA)
    a2.plot([4.6, 5.8], [2.6, 2.6], color=PAREDE, lw=4)
    a2.text(5.2, 2.85, "porta", ha="center", fontsize=7, color=TXT2)
    gw(a2, 3.8, 1.7, "GW na parede\ninterna, perto\nda porta", dx=.4, dy=.2, ha="left", va="center")
    fig.text(.01, .01, "Plantas esquemáticas, sem escala, montadas a partir das fotos do ensaio (docs/fotos). Posições aproximadas.",
             fontsize=8, color=TXT2)
    fig.savefig(SAIDA / "plantas_esquematicas.png", bbox_inches="tight"); plt.close(fig)


if __name__ == "__main__":
    SAIDA.mkdir(parents=True, exist_ok=True)
    corte(); plantas(); print("ok")
