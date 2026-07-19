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
    DY = {"claude-sonnet-5": 5, "sabia-4": -7}  # afasta rótulos vizinhos (37% vs 32%)
    for k in ordem:
        gs = sorted(d[k]); ys = [sum(d[k][g]) / len(d[k][g]) for g in gs]
        ax.plot(gs, ys, color=COR[k], lw=2.8, solid_capstyle="round", zorder=3)
        ax.annotate(f"{NOME[k]}  {ys[-1]*100:.0f}%", (gs[-1], ys[-1]), xytext=(8, DY.get(k, 0)),
                    textcoords="offset points", va="center", fontsize=12,
                    fontweight="bold", color=COR[k])
    ax.set_title("O modelo decide: de 19% a 83% do léxico gaúcho sobrevive",
                 fontsize=15, fontweight="bold", loc="left", pad=30)
    ax.text(0, 1.055, "regionalismos ainda presentes após 15 reescritas “melhore a escrita” · média de "
            "9 trechos dos Contos Gauchescos (1912) · diferenças ≤ 4 pp cabem na variância entre réplicas",
            transform=ax.transAxes, fontsize=9.6, color=INK, alpha=0.7)
    ax.set_xlabel("geração de reescrita", fontsize=12)
    ax.set_ylabel("léxico regional vivo", fontsize=12)
    ax.set_xlim(0, 18.5); ax.set_ylim(0, 1.02); ax.set_xticks([0, 1, 5, 10, 15])
    ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
    ax.set_yticklabels(["0%", "25%", "50%", "75%", "100%"])
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
    ax.set_title("Na média, o regional morre mais que a palavra comum de mesma raridade",
                 fontsize=14.5, fontweight="bold", loc="left", pad=48)
    ax.text(0, 1.045, "sobrevivência por geração, léxico regional vs controle pareado por frequência · "
            "média de 5 modelos e 9 trechos, “melhore a escrita”\no efeito varia por modelo: "
            "de −21 a +9 pp (negativo em 3 de 5)", transform=ax.transAxes, va="bottom",
            fontsize=9.2, color=INK, alpha=0.7, linespacing=1.35)
    ax.set_xlabel("geração de reescrita", fontsize=12)
    ax.set_ylabel("fração viva", fontsize=12)
    ax.set_xlim(0, 18); ax.set_ylim(0, 1.02); ax.set_xticks([0, 1, 5, 10, 15])
    ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
    ax.set_yticklabels(["0%", "25%", "50%", "75%", "100%"])
    ax.grid(axis="y", color=INK, alpha=0.09)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_alpha(0.35)
    out = os.path.join(FIG, "diferencial-regional-controle.png")
    fig.tight_layout(); fig.savefig(out, facecolor=CREAM, bbox_inches="tight")
    print("figura:", out)


def _estetica(ax, fig):
    fig.patch.set_facecolor(CREAM); ax.set_facecolor(CREAM)
    ax.grid(axis="y", color=INK, alpha=0.09)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_alpha(0.35)


def linguas():
    """Fig A: sobrevivência das palavras raras (p80) por grupo/língua, C1+C2."""
    import re, unicodedata, math
    from wordfreq import word_frequency
    _c = {}

    def toks(t):
        return re.findall(r"[a-záéíóúâêôãõàüçñ']+", unicodedata.normalize("NFC", (t or "")).lower())

    def rar(w, lang):
        k = (w, lang)
        if k not in _c:
            _c[k] = -math.log10(max(word_frequency(w, lang) or 1e-8, 1e-8))
        return _c[k]

    def grupo_de(sid):
        return ("regional" if sid.startswith("regional") else
                "controle-pt" if sid.startswith("controle-pt") else "controle-en")
    LIM = {}
    for g, pat in (("regional", "regional-*"), ("controle-pt", "controle-pt-*"),
                   ("controle-en", "controle-en-*")):
        lang = "en" if g == "controle-en" else "pt"
        rs = []
        for fn in glob.glob(os.path.join(HERE, "corpus-semente", pat + ".txt")):
            rs += [rar(w, lang) for w in toks(open(fn, encoding="utf-8").read())]
        rs.sort(); LIM[g] = rs[int(0.8 * len(rs))]
    curva = collections.defaultdict(lambda: collections.defaultdict(list))
    for fn in glob.glob(os.path.join(CAD, "*.jsonl")):
        b = os.path.basename(fn)[:-6]
        if "1912" in b or "rep" in b:
            continue
        _, cond, sid = b.split("__", 2)
        if cond not in ("pt-C1", "pt-C2", "en-C1", "en-C2"):
            continue
        g = grupo_de(sid)
        lang = "en" if g == "controle-en" else "pt"
        sp = os.path.join(HERE, "corpus-semente", sid + ".txt")
        tipos = set(toks(open(sp, encoding="utf-8").read()))
        raros = {w for w in tipos if rar(w, lang) >= LIM[g] and len(w) >= 4}
        if len(raros) < 5:
            continue
        for ln in open(fn, encoding="utf-8"):
            r = json.loads(ln)
            if r["status"] == "ok":
                s = " " + " ".join(toks(r["saida_filtrada"])) + " "
                viv = sum(1 for w in raros if (" " + w[:5]) in s)
                curva[g][r["geracao"]].append(viv / len(raros))
    est = {"controle-en": ("#7A8C99", "-", 2.0, "inglês padrão (1920–25)"),
           "controle-pt": ("#7A8C99", (0, (5, 2.4)), 2.0, "português padrão (1908–11)"),
           "regional": ("#C56A3E", "-", 3.0, "português regional gaúcho (1912)")}
    fig, ax = plt.subplots(figsize=(10, 6.2), dpi=200)
    _estetica(ax, fig)
    for g in ("controle-en", "controle-pt", "regional"):
        d = curva[g]; gs = [0] + sorted(d)
        ys = [1.0] + [sum(d[x]) / len(d[x]) for x in sorted(d)]
        cor, ls, lw, nome = est[g]
        ax.plot(gs, ys, color=cor, lw=lw, ls=ls, solid_capstyle="round", zorder=3)
        dy = {"controle-en": 7, "controle-pt": -10, "regional": 0}[g]
        ax.annotate(f"{nome}  {ys[-1]*100:.0f}%", (gs[-1], ys[-1]), xytext=(8, dy),
                    textcoords="offset points", va="center", fontsize=11.5,
                    fontweight="bold", color=cor)
    ax.set_title("Inglês e português padrão perdem igual; o texto gaúcho perde mais",
                 fontsize=14.5, fontweight="bold", loc="left", pad=30)
    ax.text(0, 1.055, "sobrevivência das 20% palavras mais raras de cada texto-semente (métrica distinta "
            "da lista de 90 regionalismos) · instruções neutra e de melhoria · média dos 5 modelos",
            transform=ax.transAxes, fontsize=9.2, color=INK, alpha=0.7)
    ax.set_xlabel("geração de reescrita", fontsize=12)
    ax.set_ylabel("palavras raras vivas", fontsize=12)
    ax.set_xlim(0, 21.5); ax.set_ylim(0, 1.02); ax.set_xticks([0, 1, 5, 10, 15])
    ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
    ax.set_yticklabels(["0%", "25%", "50%", "75%", "100%"])
    out = os.path.join(FIG, "linguas-raras.png")
    fig.tight_layout(); fig.savefig(out, facecolor=CREAM, bbox_inches="tight")
    print("figura:", out)


def estratos():
    """Fig B: realia vs variante-concorrente (C2, média modelos+sementes)."""
    import re, unicodedata
    reg = {}; estr = {}
    for r in csv.DictReader(open(os.path.join(HERE, "lista-regionalismos.csv"), encoding="utf-8")):
        lf = r.get("lema_final", "").strip()
        if lf and r["classe"] == "lexema":
            raiz = lf.split()[0]
            reg.setdefault(lf, set()).add(raiz[:5] if len(raiz) > 6 else raiz)
            estr[lf] = r.get("estrato_proposto_anotador1", "")

    def toks(t):
        return re.findall(r"[a-záéíóúâêôãõàüçñ]+", unicodedata.normalize("NFC", (t or "")).lower())

    def pres(t):
        s = " " + " ".join(toks(t)) + " "
        return {l for l, rz in reg.items() if any((" " + r) in s for r in rz)}
    curv = {"realia": collections.defaultdict(list),
            "variante-concorrente": collections.defaultdict(list)}
    for fn in glob.glob(os.path.join(CAD, "*regional*.jsonl")):
        b = os.path.basename(fn)[:-6]
        if "1912" in b or "rep" in b or b.split("__")[1] != "pt-C2":
            continue
        sid = b.split("__")[-1]
        base = pres(open(os.path.join(HERE, "corpus-semente", sid + ".txt"), encoding="utf-8").read())
        be = {e: {l for l in base if estr.get(l) == e} for e in curv}
        for ln in open(fn, encoding="utf-8"):
            r = json.loads(ln)
            if r["status"] == "ok":
                viv = pres(r["saida_filtrada"])
                for e in curv:
                    if be[e]:
                        curv[e][r["geracao"]].append(len(viv & be[e]) / len(be[e]))
    fig, ax = plt.subplots(figsize=(10, 6.2), dpi=200)
    _estetica(ax, fig)
    est = {"realia": ("#7A8C99", "sem sinônimo padrão (realia)"),
           "variante-concorrente": ("#C56A3E", "com sinônimo padrão disponível")}
    for e in ("realia", "variante-concorrente"):
        d = curv[e]; gs = [0] + sorted(d)
        ys = [1.0] + [sum(d[x]) / len(d[x]) for x in sorted(d)]
        cor, nome = est[e]
        ax.plot(gs, ys, color=cor, lw=2.8, solid_capstyle="round", zorder=3)
        ax.annotate(f"{nome}  {ys[-1]*100:.0f}%", (gs[-1], ys[-1]), xytext=(8, 0),
                    textcoords="offset points", va="center", fontsize=11.5,
                    fontweight="bold", color=cor)
    ax.text(15.2, 0.70, "chimarrão, guaiaca, nhandu, coxilha\nseguem no texto: não há com que trocar",
            fontsize=10, color="#5E7080", ha="right", style="italic")
    ax.text(15.2, 0.33, "china → moça · morocha → morena\ncancha → pista · peleia → briga",
            fontsize=10, color="#C56A3E", ha="right", style="italic")
    ax.set_title("Ter sinônimo padrão custa 20 pontos: 63% vs 43%",
                 fontsize=15, fontweight="bold", loc="left", pad=30)
    ax.text(0, 1.055, "sobrevivência do léxico regional por estrato · “melhore a escrita” · média dos "
            "5 modelos e 9 trechos · nas sementes: 23 ocorrências realia, 90 com variante concorrente",
            transform=ax.transAxes, fontsize=9.2, color=INK, alpha=0.7)
    ax.set_xlabel("geração de reescrita", fontsize=12)
    ax.set_ylabel("fração do estrato viva", fontsize=12)
    ax.set_xlim(0, 22); ax.set_ylim(0, 1.02); ax.set_xticks([0, 1, 5, 10, 15])
    ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
    ax.set_yticklabels(["0%", "25%", "50%", "75%", "100%"])
    out = os.path.join(FIG, "estratos-realia-variante.png")
    fig.tight_layout(); fig.savefig(out, facecolor=CREAM, bbox_inches="tight")
    print("figura:", out)


def instrucao_por_modelo():
    """Fig C: dumbbell C2 -> C3 por modelo (G15)."""
    d = collections.defaultdict(lambda: collections.defaultdict(list))
    for r in csv.DictReader(open(os.path.join(MET, "sobrevivencia.csv"), encoding="utf-8")):
        if (r["grupo"] == "regional" and "1912" not in r["semente"] and "rep" not in r["semente"]
                and int(r["geracao"]) == 15 and int(r["n_reg_base"])):
            m = r["modelo"].split("__")[0]
            for k in COR:
                if k in m:
                    d[k][r["cond"]].append(int(r["regionais_vivos"]) / int(r["n_reg_base"]))
    med = {k: {c: sum(v) / len(v) for c, v in cs.items()} for k, cs in d.items()}
    ordem = sorted(med, key=lambda k: med[k].get("pt-C3", 0))
    fig, ax = plt.subplots(figsize=(10, 5.6), dpi=200)
    _estetica(ax, fig)
    ax.grid(axis="x", color=INK, alpha=0.09); ax.grid(axis="y", alpha=0)
    for i, k in enumerate(ordem):
        c2, c3 = med[k].get("pt-C2", 0), med[k].get("pt-C3", 0)
        ax.plot([c2, c3], [i, i], color=COR[k], lw=2.2, alpha=0.55, zorder=2)
        ax.scatter([c2], [i], s=70, facecolor=CREAM, edgecolor=COR[k], lw=2.2, zorder=3)
        ax.scatter([c3], [i], s=95, color=COR[k], zorder=4)
        ax.annotate(f"{c2*100:.0f}%", (c2, i), xytext=(0, -16), textcoords="offset points",
                    ha="center", fontsize=10, color=COR[k])
        ax.annotate(f"{c3*100:.0f}%", (c3, i), xytext=(0, 10), textcoords="offset points",
                    ha="center", fontsize=11, fontweight="bold", color=COR[k])
        ax.annotate(NOME[k], (min(c2, c3), i), xytext=(-10, 0), textcoords="offset points",
                    ha="right", va="center", fontsize=11.5, fontweight="bold", color=COR[k])
    ax.annotate("único que segue perdendo metade\nmesmo com o pedido explícito",
                xy=(med["sabia-4"]["pt-C3"] + 0.018, ordem.index("sabia-4") + 0.04),
                xytext=(0.63, ordem.index("sabia-4") + 0.45), fontsize=10.5, color=INK,
                va="center", ha="left",
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.2,
                                connectionstyle="arc3,rad=0.25"))
    ax.scatter([], [], s=70, facecolor=CREAM, edgecolor=INK, lw=2, label="“melhore a escrita”")
    ax.scatter([], [], s=95, color=INK, label="“… preservando o vocabulário regional”")
    ax.legend(loc="lower left", frameon=False, fontsize=10.5)
    ax.set_title("Pedir para preservar funciona, mas o modelo brasileiro ainda perde metade",
                 fontsize=14.2, fontweight="bold", loc="left", pad=30)
    ax.text(0, 1.07, "sobrevivência do léxico regional na geração 15, sem e com pedido de preservação "
            "· média de 9 trechos", transform=ax.transAxes, fontsize=10.2, color=INK, alpha=0.7)
    ax.set_xlabel("fração do léxico regional viva em G15", fontsize=12)
    ax.set_xlim(0, 1.06); ax.set_ylim(-0.7, len(ordem) - 0.1)
    ax.set_yticks([])
    ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
    ax.set_xticklabels(["0%", "25%", "50%", "75%", "100%"])
    out = os.path.join(FIG, "instrucao-por-modelo.png")
    fig.tight_layout(); fig.savefig(out, facecolor=CREAM, bbox_inches="tight")
    print("figura:", out)


def distribuicao_populacao():
    """F1b: a população de textos desliza rumo ao padrão (ridgeline da densidade
    regional por texto, G0/G1/G5/G15, cadeias C2)."""
    import re, unicodedata
    import numpy as np
    from scipy.stats import gaussian_kde
    reg = {}
    for r in csv.DictReader(open(os.path.join(HERE, "lista-regionalismos.csv"), encoding="utf-8")):
        lf = r.get("lema_final", "").strip()
        if lf and r["classe"] == "lexema":
            raiz = lf.split()[0]
            reg.setdefault(lf, set()).add(raiz[:5] if len(raiz) > 6 else raiz)

    def toks(t):
        return re.findall(r"[a-záéíóúâêôãõàüçñ]+", unicodedata.normalize("NFC", (t or "")).lower())

    def dens(t):
        ws = toks(t)
        s = " " + " ".join(ws) + " "
        n = sum(1 for l, rz in reg.items() if any((" " + r) in s for r in rz))
        return 100 * n / len(ws) if ws else 0
    dados = {0: [], 1: [], 5: [], 15: []}
    for fn in glob.glob(os.path.join(HERE, "corpus-semente", "regional-0*.txt")):
        dados[0].append(dens(open(fn, encoding="utf-8").read()))
    for fn in glob.glob(os.path.join(CAD, "*regional*.jsonl")):
        b = os.path.basename(fn)[:-6]
        if "1912" in b or "rep" in b or b.split("__")[1] != "pt-C2":
            continue
        for ln in open(fn, encoding="utf-8"):
            r = json.loads(ln)
            if r["status"] == "ok" and r["geracao"] in (1, 5, 15):
                dados[r["geracao"]].append(dens(r["saida_filtrada"]))
    xs = np.linspace(-0.6, 10.5, 500)
    ordem = [0, 1, 5, 15]
    ramp = {0: "#EAC7A9", 1: "#D89B6C", 5: "#BF6E3B", 15: "#8F4517"}
    fr15 = 100 * sum(1 for x in dados[15] if x < 2) / len(dados[15])
    rot = {0: "G0 · os 9 trechos, todos acima de 3,2: todos carregam a marca",
           1: "G1 · uma única reescrita já desloca a população",
           5: "G5",
           15: f"G15 · {fr15:.0f}% dos textos com menos de 2, encostados no padrão"}
    sub = {15: "na cauda alta, resistem as cadeias do Terra e do Grok"}
    fig, ax = plt.subplots(figsize=(10, 6.6), dpi=200)
    _estetica(ax, fig)
    ax.grid(alpha=0)
    passo = 1.0
    for i, g in enumerate(ordem):
        v = np.array(dados[g])
        base = (len(ordem) - 1 - i) * passo
        kde = gaussian_kde(v, bw_method=0.4)
        ys = kde(xs); ys = ys / ys.max() * 0.78
        ax.fill_between(xs, base, base + ys, color=ramp[g], alpha=0.55, lw=0, zorder=2 + i)
        ax.plot(xs, base + ys, color=ramp[g], lw=2.2, zorder=3 + i)
        ax.plot(v, np.full_like(v, base + 0.03), "|", color=INK, ms=7, alpha=0.5, zorder=4 + i)
        med = float(np.median(v))
        ax.plot([med, med], [base, base + 0.28], color=INK, lw=1.6, zorder=5 + i)
        ax.annotate(f"mediana {med:.1f}".replace(".", ","), (med + 0.12, base + 0.30),
                    ha="left", fontsize=9, color=INK, zorder=6)
        ax.annotate(rot[g], (10.4, base + 0.86), ha="right", va="top", fontsize=10.5,
                    fontweight="bold", color=INK, alpha=0.85, zorder=6)
        if g in sub:
            ax.annotate(sub[g], (10.4, base + 0.66), ha="right", va="top", fontsize=9,
                        color=INK, alpha=0.7, zorder=6)
    ax.set_title("A população de textos desliza rumo ao padrão",
                 fontsize=15, fontweight="bold", loc="left", pad=30)
    ax.text(0, 1.045, "distribuição dos textos pela densidade de léxico regional (lemas vivos por "
            "100 palavras) · 45 cadeias, “melhore a escrita” · cada risco é um texto",
            transform=ax.transAxes, fontsize=9.6, color=INK, alpha=0.7)
    ax.set_xlabel("regionalismos vivos por 100 palavras", fontsize=12)
    ax.set_xlim(-0.6, 10.5); ax.set_ylim(-0.15, 4.75)
    ax.set_yticks([]); ax.set_xticks([0, 2, 4, 6, 8, 10])
    ax.axvline(0, color=INK, lw=0.8, alpha=0.25)
    ax.text(0, -0.135, "← registro padrão (zero regional)", transform=ax.get_xaxis_transform(),
            ha="left", fontsize=9.5, color=INK, alpha=0.65)
    out = os.path.join(FIG, "populacao-desliza-padrao.png")
    fig.tight_layout(); fig.savefig(out, facecolor=CREAM, bbox_inches="tight")
    print("figura:", out)


if __name__ == "__main__":
    curva_sobrevivencia()
    curva_instrucao()
    diferencial_geracao()
    densidade_raridade()
    linguas()
    estratos()
    instrucao_por_modelo()
    distribuicao_populacao()
    obituario()
