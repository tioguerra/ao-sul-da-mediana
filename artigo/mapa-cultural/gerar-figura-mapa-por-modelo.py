#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Figura do mapa cultural em cinco painéis (45:16, cada um 9:16), um por modelo.
Mostra o caminho de cada modelo entre as quatro condições (inglês, português,
identidade brasileira, identidade gaúcha) no plano de Inglehart-Welzel, com
Brasil e RS como âncoras humanas. Aspecto igual (distâncias honestas), mesmo
esquema de cores das figuras de reescrita, texto mínimo.

Knobs no topo: JANELA (recorte do mapa), COND_ORDEM, TS (intensidade por condição).
"""
import csv, colorsys, os
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(HERE, "figuras")
os.makedirs(FIG, exist_ok=True)

CREAM, INK = "#FFF7EF", "#1E302C"
COR = {"gpt-5-6-terra": "#4E6E58", "grok-4-5": "#7A6A9B",
       "claude-sonnet-5": "#C56A3E", "sabia-4": "#2E5A87", "gemini-3-5-flash": "#B08A2E"}
# rótulo do CSV -> (chave de cor, nome curto)
MODELO = {"GPT-5.6 Terra": ("gpt-5-6-terra", "GPT-5.6 Terra"),
          "Grok 4.5": ("grok-4-5", "Grok 4.5"),
          "Gemini 3.5 Flash": ("gemini-3-5-flash", "Gemini 3.5"),
          "Claude Sonnet 5": ("claude-sonnet-5", "Claude Sonnet 5"),
          "Sabiá-4": ("sabia-4", "Sabiá-4")}
ORDEM = ["GPT-5.6 Terra", "Grok 4.5", "Gemini 3.5 Flash", "Claude Sonnet 5", "Sabiá-4"]
COND_ORDEM = ["en_default", "pt_default", "pt_brazil", "pt_rs"]
COND_ROT = {"en_default": "inglês", "pt_default": "português",
            "pt_brazil": "id. Brasil", "pt_rs": "id. gaúcha"}
TS = (0.20, 0.45, 0.70, 0.95)  # intensidade por condição (claro -> escuro)
# janela movida p/ esquerda e p/ cima, com um pouco mais de zoom; razão ~0.5625 (9:16)
JANELA = dict(xlim=(-0.20, 2.45), ylim=(-2.56, 2.15))
# países/regiões de referência (entidade no CSV -> rótulo); DESTAQUE = âncoras humanas centrais
PAISES = {"Brazil": "Brasil", "Rio Grande do Sul": "RS", "Argentina": "Argentina",
          "Uruguay": "Uruguai", "Chile": "Chile", "Spain": "Espanha", "Ireland": "Irlanda",
          "Mexico": "México", "Germany": "Alemanha", "France": "França", "Japan": "Japão"}
DESTAQUE = {"Brazil", "Rio Grande do Sul"}
# rótulos que precisam de posição própria: (dx, dy em pt, alinhamento)
LABEL_OFFSET = {"Spain": (-4, -4, "right"), "France": (18, 6, "right"),
                "Uruguay": (0, -10, "center"), "Argentina": (0, 6, "center"),
                "Brazil": (-7, -17, "left"), "Rio Grande do Sul": (8, -1, "left"),
                "Chile": (-4, 0, "right"), "Germany": (-5, 3, "right"),
                "Ireland": (5, -1, "left")}

for f in ("Carlito", "Calibri"):
    from matplotlib import font_manager
    if any(f == fo.name for fo in font_manager.fontManager.ttflist):
        plt.rcParams["font.family"] = f
        break
plt.rcParams.update({"text.color": INK})


def _shade(base, t, lmin=0.30, lmax=0.76):
    base = base.lstrip("#")
    r, g, b = (int(base[i:i + 2], 16) / 255 for i in (0, 2, 4))
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    return colorsys.hls_to_rgb(h, lmax - t * (lmax - lmin), s)


def carregar():
    mods = {}
    for r in csv.DictReader(open(os.path.join(HERE, "coordenadas-llms-multicondicao-medias.csv"), encoding="utf-8")):
        mods.setdefault(r["model_label"], {})[r["condition"]] = (
            float(r["x_survival_self_expression"]), float(r["y_traditional_secular"]))
    anc = {}
    for r in csv.DictReader(open(os.path.join(HERE, "coordenadas-mapa-cultural.csv"), encoding="utf-8")):
        if r["entity"] in PAISES:
            anc[r["entity"]] = (float(r["x_survival_self_expression"]), float(r["y_traditional_secular"]))
    return mods, anc


def main():
    from matplotlib.patches import Patch
    mods, anc = carregar()
    # figura dimensionada p/ a razão da região casar com a dos dados (0.5625):
    # a caixa preenche a coluna, sem vão lateral (set_aspect dispensado)
    fig, axes = plt.subplots(1, 5, figsize=(15, 5.95), dpi=200,
                             gridspec_kw={"wspace": 0.05})
    fig.patch.set_facecolor(CREAM)
    for ax, ml in zip(axes, ORDEM):
        ax.set_facecolor(CREAM)
        chave, nome = MODELO[ml]
        base = COR[chave]
        ax.axhline(0, color=INK, lw=0.7, alpha=0.13, zorder=1)
        ax.axvline(0, color=INK, lw=0.7, alpha=0.13, zorder=1)
        # países/regiões de referência (cinza); Brasil e RS destacados
        for ent, rot in PAISES.items():
            if ent not in anc:
                continue
            x, y = anc[ent]
            forte = ent in DESTAQUE
            ax.plot(x, y, "o", ms=8.5 if forte else 5.5,
                    color=INK, alpha=0.5 if forte else 0.28, zorder=4 if forte else 2)
            dx, dy, ha = LABEL_OFFSET.get(ent, (5, -1, "left"))
            ax.annotate(rot, (x, y), xytext=(dx, dy), textcoords="offset points", ha=ha,
                        fontsize=11.5 if forte else 9.5, color=INK,
                        alpha=0.72 if forte else 0.5,
                        fontweight="bold" if forte else "normal", zorder=5)
        # trajetória do modelo entre as condições
        pts = [mods[ml][c] for c in COND_ORDEM]
        ax.plot(*zip(*pts), "-", color=_shade(base, 0.55), lw=2.4, alpha=0.7, zorder=3)
        for (x, y), t in zip(pts, TS):
            ax.plot(x, y, "o", ms=13, color=_shade(base, t), zorder=6,
                    markeredgecolor=CREAM, markeredgewidth=1.3)
        # legenda de cores no canto inferior esquerdo
        handles = [Patch(facecolor=_shade(base, t), edgecolor="none") for t in TS]
        ax.legend(handles, [COND_ROT[c] for c in COND_ORDEM], loc="lower left",
                  fontsize=9.5, frameon=True, facecolor=CREAM, edgecolor="none",
                  framealpha=0.9, handlelength=1.0, handleheight=1.1,
                  labelspacing=0.25, borderpad=0.4, handletextpad=0.5).set_zorder(10)
        ax.set_title(nome, fontsize=17, fontweight="bold", pad=9, color=_shade(base, 0.95))
        ax.set_xlim(*JANELA["xlim"]); ax.set_ylim(*JANELA["ylim"])
        ax.set_xticks([]); ax.set_yticks([])
        for s in ("top", "right", "bottom", "left"):
            ax.spines[s].set_alpha(0.25)
    axes[0].set_ylabel("tradicional  ↔  secular-racional", fontsize=14)
    fig.subplots_adjust(left=0.055, right=0.997, top=0.92, bottom=0.08, wspace=0.05)
    fig.text(0.5, 0.065, "sobrevivência  ↔  autoexpressão", ha="center", va="top",
             fontsize=14, color=INK)
    out = os.path.join(FIG, "mapa-por-modelo.png")
    fig.savefig(out, facecolor=CREAM, bbox_inches="tight")
    print("figura:", out)


if __name__ == "__main__":
    main()
