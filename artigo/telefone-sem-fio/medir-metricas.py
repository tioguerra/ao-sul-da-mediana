#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Métricas das cadeias de reescrita iterada (plano v1.8, seção 8).

Lê dados/cadeias/*.jsonl e produz dados/metricas/ com:
  - sobrevivencia.csv: itens regionais e controles vivos por geração/cadeia
  - diferencial.csv: taxa regional − taxa controle por geração/condição/modelo
  - massa-cauda.csv: fração de tokens acima do limiar de raridade (H6)
  - diversidade.csv: MATTR, distinct-2, hapax, comprimento, gzip por geração
Detecção por lema + variantes de superfície das listas congeladas.
"""
import csv, glob, gzip, json, os, re, unicodedata, collections, math

HERE = os.path.dirname(os.path.abspath(__file__))
CAD = os.path.join(HERE, "dados", "cadeias")
OUT = os.path.join(HERE, "dados", "metricas")
os.makedirs(OUT, exist_ok=True)


def norm(t):
    return unicodedata.normalize("NFC", (t or "")).lower()


def toks(t):
    return re.findall(r"[a-záéíóúâêôãõàüçñ]+", norm(t))


# ---- listas congeladas
def carregar_listas():
    reg = {}  # lema -> [raízes de detecção]
    estrato = {}
    for r in csv.DictReader(open(os.path.join(HERE, "lista-regionalismos.csv"), encoding="utf-8")):
        lf = r.get("lema_final", "").strip()
        if lf and r["classe"] == "lexema":
            raiz = lf.split()[0]
            reg.setdefault(lf, set()).add(raiz[:5] if len(raiz) > 6 else raiz)
            estrato[lf] = r.get("estrato_proposto_anotador1", "")
    ctl = {}
    for r in csv.DictReader(open(os.path.join(HERE, "lista-controle-pareado.csv"), encoding="utf-8")):
        if r["controle_proposto"]:
            ctl[r["regionalismo"]] = r["controle_proposto"]
    return reg, estrato, ctl


REG, ESTRATO, CTL = carregar_listas()
FLAG_HOMOG = {"mate", "pampa", "carona", "baio", "traira", "traíra", "boliche", "gambeta", "apurado"}


def presentes(texto, itens):
    """Quais itens (lema->raízes) aparecem no texto."""
    t = " " + " ".join(toks(texto)) + " "
    vivos = set()
    for lema, raizes in itens.items():
        for rz in raizes:
            if re.search(r"[ ]" + re.escape(rz), t):
                vivos.add(lema); break
    return vivos


# ---- carga das cadeias
def ler_cadeia(fn):
    gens = {}
    for ln in open(fn, encoding="utf-8"):
        r = json.loads(ln)
        if r["status"] == "ok":
            gens[r["geracao"]] = r["saida_filtrada"]
    b = os.path.basename(fn)[:-6]
    modelo, cond, sid = b.split("__", 2)
    grupo = ("regional" if sid.startswith("regional") else
             "controle-pt" if sid.startswith("controle-pt") else
             "controle-en" if sid.startswith("controle-en") else "outro")
    return modelo, cond, sid, grupo, gens


def semente_txt(sid):
    for sub in ("", "grafia-1912/"):
        p = os.path.join(HERE, "corpus-semente", sub, sid.split("#")[0] + ".txt")
        if os.path.exists(p):
            return open(p, encoding="utf-8").read().strip()
    return ""


# ---- raridade (para massa de cauda / H6): referência GERAL da língua (wordfreq)
from wordfreq import word_frequency  # noqa: E402
PISO_FREQ = 1e-8  # resolução do wordfreq; palavra desconhecida = muito rara
_cache = {}


def rar_palavra(w, lang):
    k = (w, lang)
    if k not in _cache:
        f = word_frequency(w, lang) or PISO_FREQ
        _cache[k] = -math.log10(max(f, PISO_FREQ))
    return _cache[k]


def raridades(texto, grupo):
    lang = "en" if grupo == "controle-en" else "pt"
    return [rar_palavra(w, lang) for w in toks(texto)]


def limiar_p80(grupo):
    sem_por_grupo = {"regional": "regional-09-trezentas-oncas",
                     "controle-pt": "controle-pt-01-policarpo-abertura",
                     "controle-en": "controle-en-01-gatsby"}
    rs = []
    for fn in glob.glob(os.path.join(HERE, "corpus-semente", "*.txt")):
        b = os.path.basename(fn)[:-4]
        if (grupo == "regional" and b.startswith("regional")) or \
           (grupo == "controle-pt" and b.startswith("controle-pt")) or \
           (grupo == "controle-en" and b.startswith("controle-en")):
            rs += raridades(open(fn, encoding="utf-8").read(), grupo)
    rs.sort()
    return rs[int(0.8 * len(rs))] if rs else 3.0


LIMIAR = {g: limiar_p80(g) for g in ("regional", "controle-pt", "controle-en")}


def mattr(ws, jan=50):
    if len(ws) < jan:
        return len(set(ws)) / len(ws) if ws else 0
    r = [len(set(ws[i:i+jan])) / jan for i in range(len(ws) - jan + 1)]
    return sum(r) / len(r)


def main():
    cadeias = [ler_cadeia(fn) for fn in sorted(glob.glob(os.path.join(CAD, "*.jsonl")))]
    cadeias = [c for c in cadeias if c[4]]  # com ao menos 1 geração

    # ---- sobrevivência + diferencial
    fs = open(os.path.join(OUT, "sobrevivencia.csv"), "w", newline="", encoding="utf-8")
    ws = csv.writer(fs); ws.writerow(["modelo", "cond", "semente", "grupo", "geracao",
                                      "regionais_vivos", "controles_vivos", "n_reg_base", "n_ctl_base"])
    fm = open(os.path.join(OUT, "massa-cauda.csv"), "w", newline="", encoding="utf-8")
    wm = csv.writer(fm); wm.writerow(["modelo", "cond", "semente", "grupo", "geracao", "massa_cauda", "n_tokens"])
    fd = open(os.path.join(OUT, "diversidade.csv"), "w", newline="", encoding="utf-8")
    wd = csv.writer(fd); wd.writerow(["modelo", "cond", "semente", "grupo", "geracao",
                                      "n_palavras", "mattr", "distinct2", "hapax", "gzip_ratio"])

    ctl_itens = {c: {c: {c[:5] if len(c) > 6 else c}} for c in set(CTL.values())}
    ctl_itens = {v: {v[:5] if len(v) > 6 else v} for v in set(CTL.values())}

    for modelo, cond, sid, grupo, gens in cadeias:
        base_txt = semente_txt(sid)
        reg_base = presentes(base_txt, REG) if grupo == "regional" else set()
        ctl_base = presentes(base_txt, ctl_itens) if grupo == "regional" else set()
        lim = LIMIAR[grupo]
        seq = [(0, base_txt)] + sorted(gens.items())
        for g, txt in seq:
            wv = toks(txt)
            rv = presentes(txt, REG) & reg_base if grupo == "regional" else set()
            cv = presentes(txt, ctl_itens) & ctl_base if grupo == "regional" else set()
            ws.writerow([modelo, cond, sid, grupo, g, len(rv), len(cv), len(reg_base), len(ctl_base)])
            rar = raridades(txt, grupo)
            mc = sum(1 for x in rar if x >= lim) / len(rar) if rar else 0
            wm.writerow([modelo, cond, sid, grupo, g, round(mc, 4), len(rar)])
            comp = len(gzip.compress(txt.encode("utf-8"))) / max(len(txt.encode("utf-8")), 1)
            hap = sum(1 for w, n in collections.Counter(wv).items() if n == 1)
            d2 = len(set(zip(wv, wv[1:]))) / max(len(wv) - 1, 1)
            wd.writerow([modelo, cond, sid, grupo, g, len(wv), round(mattr(wv), 4),
                         round(d2, 4), hap, round(comp, 4)])
    for f in (fs, fm, fd):
        f.close()

    # ---- resumo headline
    print("== SOBREVIVÊNCIA REGIONAL (fração da base viva) por modelo, cond C2, média das 9 sementes regionais ==")
    dados = collections.defaultdict(lambda: collections.defaultdict(list))
    for row in csv.DictReader(open(os.path.join(OUT, "sobrevivencia.csv"), encoding="utf-8")):
        if row["grupo"] == "regional" and row["cond"] == "pt-C2":
            base = int(row["n_reg_base"])
            if base:
                dados[row["modelo"].split("__")[0]][int(row["geracao"])].append(int(row["regionais_vivos"]) / base)
    for m in sorted(dados):
        mm = dados[m]
        linha = " ".join(f"G{g}:{sum(mm[g])/len(mm[g]):.2f}" for g in (0, 1, 5, 10, 15) if g in mm)
        print(f"  {m.replace('anthropic-','').replace('openai-','').replace('google-','').replace('x-ai-',''):20s} {linha}")


if __name__ == "__main__":
    main()
