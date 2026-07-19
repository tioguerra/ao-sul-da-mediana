#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Figuras do experimento telefone-sem-fio a partir de dados/metricas/.
F4-headline: sobrevivência do léxico regional por geração e modelo (dados reais)."""
import csv, collections, os, glob, json
import matplotlib.pyplot as plt
from matplotlib import font_manager

HERE = os.path.dirname(os.path.abspath(__file__))
MET = os.path.join(HERE, "dados", "metricas")
CAD = os.path.join(HERE, "dados", "cadeias")
FIG = os.path.join(HERE, "figuras")
os.makedirs(FIG, exist_ok=True)

CREAM, INK = "#FFF7EF", "#1E302C"
COR = {"gpt-5-6-terra": "#4E6E58", "grok-4-5": "#7A6A9B",
       "claude-sonnet-5": "#C56A3E", "sabia-4": "#2E5A87", "gemini-3-5-flash": "#B08A2E"}
NOME = {"gpt-5-6-terra": "GPT-5.6 Terra", "grok-4-5": "Grok 4.5",
        "claude-sonnet-5": "Claude Sonnet 5", "sabia-4": "Sabiá-4", "gemini-3-5-flash": "Gemini 3.5"}
for f in ("Carlito", "Calibri"):
    if any(f == fo.name for fo in font_manager.fontManager.ttflist):
        plt.rcParams["font.family"] = f; break
plt.rcParams.update({"text.color": INK, "axes.edgecolor": INK,
                     "xtick.color": INK, "ytick.color": INK})


def curva_sobrevivencia(cond="pt-C2"):
    d = collections.defaultdict(lambda: collections.defaultdict(list))
    for r in csv.DictReader(open(os.path.join(MET, "sobrevivencia.csv"), encoding="utf-8")):
        if r["grupo"] == "regional" and r["cond"] == cond and int(r["n_reg_base"]):
            m = r["modelo"].split("__")[0]
            for k in COR:
                if k in m:
                    d[k][int(r["geracao"])].append(int(r["regionais_vivos"]) / int(r["n_reg_base"]))
    fig, ax = plt.subplots(figsize=(10, 6.2), dpi=200)
    fig.patch.set_facecolor(CREAM); ax.set_facecolor(CREAM)
    ordem = sorted(d, key=lambda k: -sum(d[k][15]) / len(d[k][15]))
    for k in ordem:
        gs = sorted(d[k]); ys = [sum(d[k][g]) / len(d[k][g]) for g in gs]
        ax.plot(gs, ys, color=COR[k], lw=2.8, solid_capstyle="round", zorder=3)
        ax.annotate(f"{NOME[k]}  {ys[-1]*100:.0f}%", (gs[-1], ys[-1]), xytext=(8, 0),
                    textcoords="offset points", va="center", fontsize=12,
                    fontweight="bold", color=COR[k])
    ax.set_title("Quanto do léxico gaúcho sobrevive a 15 reescritas “melhore a escrita”",
                 fontsize=15, fontweight="bold", loc="left", pad=30)
    ax.text(0, 1.055, "fração dos regionalismos da semente ainda presentes · média de 9 contos de "
            "Simões Lopes Neto (1912)", transform=ax.transAxes, fontsize=10.5, color=INK, alpha=0.7)
    ax.set_xlabel("geração de reescrita", fontsize=12)
    ax.set_ylabel("fração do léxico regional viva", fontsize=12)
    ax.set_xlim(0, 18.5); ax.set_ylim(0, 1.02); ax.set_xticks([0, 1, 5, 10, 15])
    ax.grid(axis="y", color=INK, alpha=0.09)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_alpha(0.35)
    out = os.path.join(FIG, "sobrevivencia-regional-por-modelo.png")
    fig.tight_layout(); fig.savefig(out, facecolor=CREAM, bbox_inches="tight")
    print("figura:", out)


def curva_instrucao():
    """Três instruções (C1 neutra, C2 melhoria, C3 preservar), média modelos+sementes."""
    d = collections.defaultdict(lambda: collections.defaultdict(list))
    for r in csv.DictReader(open(os.path.join(MET, "sobrevivencia.csv"), encoding="utf-8")):
        if r["grupo"] == "regional" and "1912" not in r["semente"] and int(r["n_reg_base"]):
            d[r["cond"]][int(r["geracao"])].append(int(r["regionais_vivos"]) / int(r["n_reg_base"]))
    est = {"pt-C1": ("#8F4517", "“Reescreva” (neutra)"),
           "pt-C2": ("#C56A3E", "“Melhore a escrita”"),
           "pt-C3": ("#4E6E58", "“Melhore, preservando o regional”")}
    fig, ax = plt.subplots(figsize=(10, 6.2), dpi=200)
    fig.patch.set_facecolor(CREAM); ax.set_facecolor(CREAM)
    for c in ("pt-C3", "pt-C2", "pt-C1"):
        gs = sorted(d[c]); ys = [sum(d[c][g]) / len(d[c][g]) for g in gs]
        ax.plot(gs, ys, color=est[c][0], lw=2.8, solid_capstyle="round", zorder=3)
        ax.annotate(f"{est[c][1]}  {ys[-1]*100:.0f}%", (gs[-1], ys[-1]), xytext=(8, 0),
                    textcoords="offset points", va="center", fontsize=11.5,
                    fontweight="bold", color=est[c][0])
    ax.set_title("A instrução decide: pedir para preservar o regional funciona",
                 fontsize=15, fontweight="bold", loc="left", pad=30)
    ax.text(0, 1.055, "sobrevivência do léxico regional · média dos 5 modelos e 9 sementes",
            transform=ax.transAxes, fontsize=10.5, color=INK, alpha=0.7)
    ax.set_xlabel("geração de reescrita", fontsize=12)
    ax.set_ylabel("fração do léxico regional viva", fontsize=12)
    ax.set_xlim(0, 22); ax.set_ylim(0, 1.02); ax.set_xticks([0, 1, 5, 10, 15])
    ax.grid(axis="y", color=INK, alpha=0.09)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_alpha(0.35)
    out = os.path.join(FIG, "efeito-instrucao.png")
    fig.tight_layout(); fig.savefig(out, facecolor=CREAM, bbox_inches="tight")
    print("figura:", out)


def obituario():
    """Geração mediana de morte por item regional (k=3), C1+C2, todos modelos."""
    import re, unicodedata
    reg = {}
    for r in csv.DictReader(open(os.path.join(HERE, "lista-regionalismos.csv"), encoding="utf-8")):
        lf = r.get("lema_final", "").strip()
        if lf and r["classe"] == "lexema":
            raiz = lf.split()[0]
            reg.setdefault(lf, set()).add(raiz[:5] if len(raiz) > 6 else raiz)

    def toks(t):
        return re.findall(r"[a-záéíóúâêôãõàüçñ]+", unicodedata.normalize("NFC", (t or "")).lower())

    def pres(t):
        s = " " + " ".join(toks(t)) + " "
        return {l for l, rz in reg.items() if any(re.search(r"[ ]" + re.escape(r), s) for r in rz)}
    import json
    mortes = collections.defaultdict(list)
    for fn in glob.glob(os.path.join(CAD, "*regional*.jsonl")):
        b = os.path.basename(fn)[:-6]
        if "1912" in b or "rep" in b:
            continue
        cond = b.split("__")[1]
        if cond not in ("pt-C1", "pt-C2"):
            continue
        sid = b.split("__")[-1]
        sp = os.path.join(HERE, "corpus-semente", sid + ".txt")
        if not os.path.exists(sp):
            continue
        base = pres(open(sp, encoding="utf-8").read())
        gens = {}
        for ln in open(fn, encoding="utf-8"):
            r = json.loads(ln)
            if r["status"] == "ok":
                gens[r["geracao"]] = pres(r["saida_filtrada"])
        maxg = max(gens) if gens else 0
        for item in base:
            morte = maxg + 1
            aus = 0
            for g in range(1, maxg + 1):
                if item not in gens.get(g, set()):
                    aus += 1
                    if aus >= 3:
                        morte = g - 2; break
                else:
                    aus = 0
            mortes[item].append(morte)
    import statistics
    med = {i: statistics.median(v) for i, v in mortes.items() if len(v) >= 5}
    ordenado = sorted(med.items(), key=lambda x: x[1])
    print("\n== OBITUÁRIO: geração mediana de morte (mais efêmeros primeiro) ==")
    for i, m in ordenado[:12]:
        print(f"  morre G{int(m):<2d} {i}")
    print("  ...")
    for i, m in ordenado[-8:]:
        rot = "sobrevive" if m > 15 else f"morre G{int(m)}"
        print(f"  {rot:11s} {i}")


def _rar_fns():
    import re, unicodedata, math
    from wordfreq import word_frequency
    cache = {}

    def toks(t):
        return re.findall(r"[a-záéíóúâêôãõàüçñ]+", unicodedata.normalize("NFC", (t or "")).lower())

    def rar(w, lang="pt"):
        k = (w, lang)
        if k not in cache:
            cache[k] = -math.log10(max(word_frequency(w, lang) or 1e-8, 1e-8))
        return cache[k]
    return toks, rar


def densidade_raridade():
    """F1: densidade da raridade lexical por geração (cadeias regionais, C2)."""
    import numpy as np
    from scipy.stats import gaussian_kde
    toks, rar = _rar_fns()
    porg = {0: [], 1: [], 5: [], 15: []}
    for fn in glob.glob(os.path.join(CAD, "*regional*.jsonl")):
        b = os.path.basename(fn)[:-6]
        if "1912" in b or "rep" in b or b.split("__")[1] != "pt-C2":
            continue
        sid = b.split("__")[-1]
        sp = os.path.join(HERE, "corpus-semente", sid + ".txt")
        if os.path.exists(sp):
            porg[0] += [rar(w) for w in toks(open(sp, encoding="utf-8").read())]
        for ln in open(fn, encoding="utf-8"):
            r = json.loads(ln)
            if r["status"] == "ok" and r["geracao"] in porg:
                porg[r["geracao"]] += [rar(w) for w in toks(r["saida_filtrada"])]
    xs = np.linspace(0, 8, 400)
    ramp = {0: "#EAC7A9", 1: "#D89B6C", 5: "#BF6E3B", 15: "#8F4517"}
    fig, ax = plt.subplots(figsize=(10, 6.2), dpi=200)
    fig.patch.set_facecolor(CREAM); ax.set_facecolor(CREAM)
    for g in (0, 1, 5, 15):
        kde = gaussian_kde(porg[g]); ys = kde(xs)
        ax.plot(xs, ys, color=ramp[g], lw=2.6, solid_capstyle="round", zorder=3)
        if g == 0:
            ax.fill_between(xs, ys, 0, where=xs > 4.2, color=ramp[0], alpha=0.25, lw=0)
        xl = {0: 5.6, 1: 5.0, 5: 4.6, 15: 4.2}[g]
        ax.annotate(f"G{g}", (xl, float(kde(xl))), xytext=(4, 6), textcoords="offset points",
                    fontsize=13, fontweight="bold", color=ramp[g])
    ax.annotate("a cauda esvazia:\no raro deixa de ser dito", xy=(6.0, float(gaussian_kde(porg[0])(6.0))),
                xytext=(5.6, ax.get_ylim()[1]*0.62), fontsize=12, color=INK,
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.3))
    ax.set_title("A cauda de raridade encolhe a cada reescrita", fontsize=15,
                 fontweight="bold", loc="left", pad=30)
    ax.text(0, 1.055, "densidade da raridade lexical (−log₁₀ da frequência, wordfreq) · cadeias "
            "regionais, “melhore a escrita”", transform=ax.transAxes, fontsize=10.5, color=INK, alpha=0.7)
    ax.text(1.2, -0.055, "palavras comuns", transform=ax.get_xaxis_transform(), ha="center",
            fontsize=10.5, color=INK, alpha=0.6)
    ax.text(6.8, -0.055, "palavras raras →", transform=ax.get_xaxis_transform(), ha="center",
            fontsize=10.5, color=INK, alpha=0.6)
    ax.set_xlabel("raridade da palavra", fontsize=12, labelpad=22)
    ax.set_ylabel("densidade", fontsize=12); ax.set_xlim(0, 8); ax.set_yticks([])
    ax.grid(axis="y", color=INK, alpha=0.08)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_alpha(0.35)
    out = os.path.join(FIG, "densidade-raridade.png")
    fig.tight_layout(); fig.savefig(out, facecolor=CREAM, bbox_inches="tight")
    print("figura:", out)


def diferencial_geracao():
    """F3: sobrevivência regional vs controle pareado, por geração (C2, média modelos+sementes)."""
    dr = collections.defaultdict(list); dc = collections.defaultdict(list)
    for r in csv.DictReader(open(os.path.join(MET, "sobrevivencia.csv"), encoding="utf-8")):
        if r["grupo"] == "regional" and r["cond"] == "pt-C2" and "1912" not in r["semente"]:
            g = int(r["geracao"])
            if int(r["n_reg_base"]):
                dr[g].append(int(r["regionais_vivos"]) / int(r["n_reg_base"]))
            if int(r["n_ctl_base"]):
                dc[g].append(int(r["controles_vivos"]) / int(r["n_ctl_base"]))
    gs = sorted(dr)
    yr = [sum(dr[g]) / len(dr[g]) for g in gs]
    yc = [sum(dc[g]) / len(dc[g]) for g in gs]
    fig, ax = plt.subplots(figsize=(10, 6.2), dpi=200)
    fig.patch.set_facecolor(CREAM); ax.set_facecolor(CREAM)
    ax.plot(gs, yc, color="#7A8C99", lw=2.6, solid_capstyle="round", zorder=3)
    ax.plot(gs, yr, color="#C56A3E", lw=2.8, solid_capstyle="round", zorder=3)
    ax.fill_between(gs, yr, yc, color="#C56A3E", alpha=0.13, zorder=1)
    ax.annotate(f"controle pareado  {yc[-1]*100:.0f}%", (gs[-1], yc[-1]), xytext=(8, 0),
                textcoords="offset points", va="center", fontsize=12, fontweight="bold", color="#5E7080")
    ax.annotate(f"regionalismos  {yr[-1]*100:.0f}%", (gs[-1], yr[-1]), xytext=(8, 0),
                textcoords="offset points", va="center", fontsize=12, fontweight="bold", color="#C56A3E")
    ax.set_title("O regional morre mais que a palavra comum de mesma raridade", fontsize=15,
                 fontweight="bold", loc="left", pad=30)
    ax.text(0, 1.055, "sobrevivência por geração, léxico regional vs controle pareado por frequência "
            "· média 5 modelos, 9 sementes, “melhore a escrita”", transform=ax.transAxes,
            fontsize=9.8, color=INK, alpha=0.7)
    ax.set_xlabel("geração de reescrita", fontsize=12)
    ax.set_ylabel("fração viva", fontsize=12)
    ax.set_xlim(0, 18); ax.set_ylim(0, 1.02); ax.set_xticks([0, 1, 5, 10, 15])
    ax.grid(axis="y", color=INK, alpha=0.09)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_alpha(0.35)
    out = os.path.join(FIG, "diferencial-regional-controle.png")
    fig.tight_layout(); fig.savefig(out, facecolor=CREAM, bbox_inches="tight")
    print("figura:", out)


if __name__ == "__main__":
    curva_sobrevivencia()
    curva_instrucao()
    diferencial_geracao()
    densidade_raridade()
    obituario()
