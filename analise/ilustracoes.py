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
    ax.text(10.5, 2 * H + 1.25, "apto 21 (Wi-Fi)", ha="center", fontsize=7.5, color=LARANJA)
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


def porta(ax, x0, y0, x1, y1, rot=None, tx=0, ty=0, ha="center"):
    """Porta de apartamento/saída: trecho hachurado sobre a parede."""
    ax.add_patch(Rectangle((min(x0, x1) - .08, min(y0, y1) - .08), abs(x1 - x0) + .16, abs(y1 - y0) + .16,
                           fc="white", ec=TXT2, hatch="////", lw=.8, zorder=4))
    if rot:
        ax.text((x0 + x1) / 2 + tx, (y0 + y1) / 2 + ty, rot, ha=ha, va="center", fontsize=7.5, color=TXT2)


def escada(ax, x, y, w, h, vertical=False):
    ax.add_patch(Rectangle((x, y), w, h, fc="#ebe9e3", ec=PAREDE, lw=1))
    n = 7
    for k in range(1, n):
        if vertical:
            ax.plot([x + k * w / n] * 2, [y, y + h], color="#c9c7c0", lw=.8)
        else:
            ax.plot([x, x + w], [y + k * h / n] * 2, color="#c9c7c0", lw=.8)
    ax.text(x + w / 2, y + h / 2, "escada", ha="center", va="center", fontsize=8, color=TXT2,
            bbox=dict(boxstyle="round,pad=.15", fc="#ebe9e3", ec="none"))


def elevador(ax, x, y, w, h, porta_em="direita"):
    ax.add_patch(Rectangle((x, y), w, h, fc="#dcdad3", ec=PAREDE, hatch="////", lw=1))
    ax.text(x + w / 2, y + h / 2, "elevador", ha="center", va="center", fontsize=8.5, color=TXT,
            bbox=dict(boxstyle="round,pad=.2", fc="white", ec="none"))
    if porta_em == "direita":      # (não usado: porta lateral)
        ax.plot([x + w] * 2, [y + h * .55, y + h * .9], color=AZUL, lw=4, solid_capstyle="butt")
        ax.text(x + w + .15, y + h * .5, "porta do\nelevador", fontsize=6.5, color=AZUL, va="top")
    else:                          # porta voltada para o hall de baixo (todos os andares)
        ax.plot([x + w * .55, x + w * .9], [y] * 2, color=AZUL, lw=4, solid_capstyle="butt")
        ax.text(x + w * .725, y - .15, "porta do elevador", fontsize=6.5, color=AZUL, ha="center", va="top")


def base(ax, titulo):
    ax.set_xlim(-3.9, 13.2); ax.set_ylim(-1.4, 7.6); ax.set_aspect("equal"); ax.axis("off")
    ax.set_title(titulo, loc="left", fontsize=10.5, fontweight="bold", color=TXT)
    ax.add_patch(Rectangle((0, 0), 10, 7, fc=PISO, ec=PAREDE, lw=1.8))


def plantas():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(13, 3.7))
    fig.subplots_adjust(bottom=.06, top=.9, wspace=.05)

    # ---- Térreo ----------------------------------------------------------
    base(a1, "Térreo: nó das rodadas A0, A1 e A2")
    escada(a1, 0, 5.6, 3.6, 1.4)
    a1.add_patch(Rectangle((3.6, 5.6), 1.4, 1.4, fc="#eeeae0", ec=PAREDE, lw=1))
    a1.text(4.3, 6.3, "dispensa", ha="center", va="center", fontsize=7, color=TXT2)
    escada(a1, 0, 3.4, 2.0, 2.2, vertical=True)
    elevador(a1, 2.0, 3.4, 3.0, 2.2, porta_em="baixo")
    a1.text(8.0, 6.2, "hall de entrada", ha="center", fontsize=9, color=TXT2)
    a1.text(8.0, 1.6, "hall de entrada", ha="center", fontsize=9, color=TXT2)
    porta(a1, 1.0, 0, 2.4, 0, "garagem", ty=-.45)
    a1.add_patch(Rectangle((3.6, 1.6), 1.2, .8, fc="white", ec=TXT2, lw=.8))
    a1.plot(4.2, 2.0, "o", ms=11, color=AZUL, mec="white", mew=1.5, zorder=5)
    a1.text(4.2, 1.45, "nó na mesa (tomada),\n~3 m do elevador", ha="center", va="top",
            fontsize=7.5, color=AZUL, fontweight="bold")

    # ---- Andar tipo (2º) -------------------------------------------------
    base(a2, "2º andar: gateway fixo no apto 21 (todas as rodadas)")
    escada(a2, 0, 5.6, 6.6, 1.4)
    escada(a2, 0, 3.2, 2.0, 2.4, vertical=True)
    elevador(a2, 2.0, 3.2, 3.6, 2.4, porta_em="baixo")
    a2.text(8.3, 5.0, "hall dos\napartamentos", ha="center", va="center", fontsize=8.5, color=TXT2)
    a2.text(5.0, 1.6, "hall dos apartamentos", ha="center", fontsize=9, color=TXT2)
    # apartamento 1 (apto 21) à esquerda, com o gateway
    a2.add_patch(Rectangle((-3.7, -.6), 3.5, 7.6, fc="#fdf0e8", ec=LARANJA, lw=1.2, ls="--"))
    a2.text(-1.95, 6.5, "apto 21\n(AP1)", ha="center", va="center", fontsize=8, color=LARANJA)
    porta(a2, 0, 1.2, 0, 2.4, "entrada 1\nAP1", tx=.25, ha="left")
    porta(a2, 1.6, 0, 2.8, 0, "entrada 2 AP1", ty=-.45)
    porta(a2, 6.6, 0, 7.8, 0, "entrada 2 AP2", ty=-.45)
    porta(a2, 10, 1.4, 10, 2.6, "entrada 1\nAP2", tx=.25, ha="left")
    gw(a2, -.55, 2.75, "GW na parede,\nao lado da\nentrada 1", dx=-1.4, dy=-1.3)
    a2.text(11.6, 5.0, "AP2", ha="center", fontsize=8, color=TXT2)

    fig.text(.01, .01, "Plantas esquemáticas, sem escala, feitas a partir do esboço e das fotos do ensaio. Posições aproximadas.",
             fontsize=8, color=TXT2)
    fig.savefig(SAIDA / "plantas_esquematicas.png", bbox_inches="tight"); plt.close(fig)


if __name__ == "__main__":
    SAIDA.mkdir(parents=True, exist_ok=True)
    corte(); plantas(); print("ok")
