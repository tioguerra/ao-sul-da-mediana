#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Coletor das cadeias de reescrita iterada (plano-experimental.md v1.7).

Chaves somente por variáveis de ambiente (OPENROUTER_API_KEY, MARITACA_API_KEY);
nunca são gravadas. Um JSONL de auditoria por cadeia em dados/cadeias/; retomada
automática a partir do próprio JSONL; tetos de gasto de US$ 18 (total) e R$ 30
(Maritaca) impostos aqui.

Uso:
  python3 rodar-cadeias.py --dry-run                # plano e projeção, sem rede
  python3 rodar-cadeias.py --pilot                  # piloto reduzido
  python3 rodar-cadeias.py                          # coleta completa (núcleo+grafia)
  python3 rodar-cadeias.py --arms core,grafia,calibracao
  python3 rodar-cadeias.py --models sabia-4,google/gemini-3.5-flash
"""
import argparse, glob, hashlib, json, os, re, sys, threading, time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone

import requests

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from prompts import PROMPTS, CONDICOES_POR_GRUPO, hash_prompt  # noqa: E402

DADOS = os.path.join(HERE, "dados", "cadeias")  # piloto grava em dados/piloto (main)
GASTO = os.path.join(HERE, "dados", "gasto.json")
TETO_USD_TOTAL = 24.00  # subido de 18 -> 24 (autorizado) p/ os 2 braços; margem sobre o custo real
TETO_BRL_MARITACA = 30.00
MAX_TOKENS = 4096
BRL_POR_USD = 5.60  # só para consolidar o teto global; gasto Maritaca é rastreado em BRL

# Política de decodificação por modelo (plano v1.8, fontes na proveniência).
# "params": o que é ENVIADO; "documentado": o default registrado.
# reasoning.effort=minimal em TODOS os modelos com função de raciocínio (Gemini e
# Grok obrigam raciocínio, não desativável; Terra raciocina leve; Claude não
# raciocina nesta config, 0 tokens). Uniformizar em minimal torna os modelos
# comparáveis e viabiliza o orçamento; o raciocínio é descartado e nunca entra no
# texto encadeado. custo_call_musd/mbrl = custo/chamada MEDIDO em 3 amostras do
# piloto (só para projeção; o gasto real vem do campo cost do OpenRouter).
REASONING_MIN = {"effort": "minimal"}
MODELOS = {
    "anthropic/claude-sonnet-5": {
        "backend": "openrouter",
        "params": {"temperature": 1.0, "reasoning": REASONING_MIN},
        "documentado": {"temperature": 1.0, "top_p": "não documentado (Anthropic)",
                        "reasoning": "minimal (0 tokens observados)"},
        "custo_call_musd": 5.12,
    },
    "openai/gpt-5.6-terra": {
        "backend": "openrouter",
        "params": {"temperature": 1.0, "top_p": 1.0, "reasoning": REASONING_MIN},
        "documentado": {"temperature": 1.0, "top_p": 1.0, "reasoning": "minimal"},
        "custo_call_musd": 4.61,
    },
    "google/gemini-3.5-flash": {
        "backend": "openrouter",
        "params": {"reasoning": REASONING_MIN},  # temp/top_p omitidos (rec. Google)
        "documentado": {"temperature": 1.0, "top_p": 0.95, "reasoning": "minimal (obrigatório)"},
        "custo_call_musd": 2.85,
    },
    "x-ai/grok-4.5": {
        "backend": "openrouter",
        "params": {"temperature": 1.0, "top_p": 1.0, "reasoning": REASONING_MIN},
        "documentado": {"temperature": 1.0, "top_p": 1.0, "reasoning": "minimal (obrigatório)"},
        "custo_call_musd": 4.34,
    },
    "sabia-4": {
        "backend": "maritaca",
        "params": {"temperature": 0.7, "top_p": 0.95},  # sem função de raciocínio
        "documentado": {"temperature": 0.7, "top_p": 0.95},
        "custo_call_mbrl": 9.8,
    },
}

SEM_OPENROUTER = threading.Semaphore(8)
SEM_MARITACA = threading.Semaphore(2)
LOCK_GASTO = threading.Lock()
PARAR = threading.Event()


# ---------------------------------------------------------------- sementes
def carregar_sementes():
    grupos = {"regional": [], "controle-pt": [], "controle-en": [], "grafia1912": []}
    for fn in sorted(glob.glob(os.path.join(HERE, "corpus-semente", "*.txt"))):
        base = os.path.basename(fn)[:-4]
        texto = open(fn, encoding="utf-8").read().strip()
        if base.startswith("regional-"):
            grupos["regional"].append((base, texto))
        elif base.startswith("controle-pt-"):
            grupos["controle-pt"].append((base, texto))
        elif base.startswith("controle-en-"):
            grupos["controle-en"].append((base, texto))
    for fn in sorted(glob.glob(os.path.join(HERE, "corpus-semente", "grafia-1912", "*.txt"))):
        grupos["grafia1912"].append((os.path.basename(fn)[:-4], open(fn, encoding="utf-8").read().strip()))
    return grupos


def montar_cadeias(args):
    g = carregar_sementes()
    braços = args.arms.split(",")
    modelos = args.models.split(",") if args.models else list(MODELOS)
    cadeias = []  # (modelo, condicao, semente_id, texto_semente, geracoes)
    gens = args.max_gens

    def add(mods, grupo, sementes, conds=None):
        for m in mods:
            for cond in (conds or CONDICOES_POR_GRUPO[grupo]):
                for sid, txt in sementes:
                    cadeias.append((m, cond, sid, txt, gens))

    if args.pilot:
        pil_reg = [s for s in g["regional"] if "trezentas" in s[0]][:1]
        pil_pt = g["controle-pt"][:1]
        pil_en = g["controle-en"][:1]
        add(modelos, "regional", pil_reg)
        add(modelos, "controle-pt", pil_pt)
        add(modelos, "controle-en", pil_en)
        return cadeias
    if "core" in braços:
        add(modelos, "regional", g["regional"])
        add(modelos, "controle-pt", g["controle-pt"])
        add(modelos, "controle-en", g["controle-en"])
    if "grafia" in braços:
        add(modelos, "regional", g["grafia1912"])
    if "calibracao" in braços:
        sub = g["regional"][:1] + g["controle-pt"][:1] + g["regional"][8:9]
        for rep in (1, 2, 3):
            for m in modelos[:1]:
                for cond in CONDICOES_POR_GRUPO["regional"]:
                    for sid, txt in sub:
                        cadeias.append((m, cond, f"{sid}#rep{rep}", txt, gens))
    return cadeias


# ---------------------------------------------------------------- gasto
def ler_gasto():
    if os.path.exists(GASTO):
        return json.load(open(GASTO))
    return {"usd_total": 0.0, "brl_maritaca": 0.0}


def somar_gasto(usd=0.0, brl=0.0):
    with LOCK_GASTO:
        gs = ler_gasto()
        gs["usd_total"] += usd + brl / BRL_POR_USD
        gs["brl_maritaca"] += brl
        os.makedirs(os.path.dirname(GASTO), exist_ok=True)
        json.dump(gs, open(GASTO, "w"))
        if gs["usd_total"] >= TETO_USD_TOTAL or gs["brl_maritaca"] >= TETO_BRL_MARITACA:
            PARAR.set()
        return gs


# ---------------------------------------------------------------- filtro de moldura
META = re.compile(r"(aqui está|segue|texto reescrito|reescrit[ao]|rewritten|"
                  r"here is|here's|certainly|claro|espero que|hope this|"
                  r"let me know|qualquer (coisa|dúvida))", re.I)


def filtrar_moldura(texto):
    removido = []
    t = texto.strip()
    m = re.match(r"^```[a-z]*\n(.*)\n```$", t, re.S)
    if m:
        removido.append("cerca de código")
        t = m.group(1).strip()
    linhas = t.split("\n")
    if len(linhas) > 1 and len(linhas[0].split()) <= 12 and META.search(linhas[0]):
        removido.append(f"preâmbulo: {linhas[0][:60]}")
        t = "\n".join(linhas[1:]).strip()
    linhas = t.split("\n")
    if len(linhas) > 1 and len(linhas[-1].split()) <= 12 and META.search(linhas[-1]):
        removido.append(f"posfácio: {linhas[-1][:60]}")
        t = "\n".join(linhas[:-1]).strip()
    if len(t) >= 2 and t[0] in "\"“" and t[-1] in "\"”":
        removido.append("aspas envolventes")
        t = t[1:-1].strip()
    return t, removido


# ---------------------------------------------------------------- chamada
def chamar(modelo, prompt_texto):
    info = MODELOS[modelo]
    if info["backend"] == "openrouter":
        url = "https://openrouter.ai/api/v1/chat/completions"
        chave = os.environ["OPENROUTER_API_KEY"]
        corpo = {"model": modelo,
                 "messages": [{"role": "user", "content": prompt_texto}],
                 "max_tokens": MAX_TOKENS,
                 "provider": {"allow_fallbacks": False},
                 "usage": {"include": True}}
        sem = SEM_OPENROUTER
    else:
        url = "https://chat.maritaca.ai/api/chat/completions"
        chave = os.environ["MARITACA_API_KEY"]
        corpo = {"model": modelo,
                 "messages": [{"role": "user", "content": prompt_texto}],
                 "max_tokens": MAX_TOKENS}
        sem = SEM_MARITACA
    corpo.update(info["params"])
    with sem:
        r = requests.post(url, json=corpo, timeout=180,
                          headers={"Authorization": f"Bearer {chave}"})
    r.raise_for_status()
    j = r.json()
    if "error" in j:
        raise RuntimeError(str(j["error"])[:300])
    esc = j["choices"][0]
    usage = j.get("usage", {}) or {}
    return {"texto": esc["message"]["content"] or "",
            "finish_reason": esc.get("finish_reason", ""),
            "response_model": j.get("model", ""),
            "provider": j.get("provider", info["backend"]),
            "tokens_in": usage.get("prompt_tokens", 0),
            "tokens_out": usage.get("completion_tokens", 0),
            "custo_usd_provedor": (usage.get("cost") if info["backend"] == "openrouter" else None)}


def custo_por_chamada(modelo):
    """Projeção: custo/chamada medido (mUSD ou mBRL) -> (usd, brl)."""
    info = MODELOS[modelo]
    if "custo_call_musd" in info:
        return info["custo_call_musd"] / 1000.0, 0.0
    return 0.0, info["custo_call_mbrl"] / 1000.0


# ---------------------------------------------------------------- cadeia
def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def rodar_cadeia(modelo, cond, sid, semente, geracoes):
    cid = f"{slug(modelo)}__{cond}__{slug(sid)}"
    caminho = os.path.join(DADOS, cid + ".jsonl")
    os.makedirs(DADOS, exist_ok=True)
    feitos, texto, provider_g1, encerrada = [], semente, None, False
    if os.path.exists(caminho):
        for ln in open(caminho, encoding="utf-8"):
            reg = json.loads(ln)
            if reg.get("status") == "ok":
                feitos.append(reg["geracao"])
                texto = reg["saida_filtrada"]
                provider_g1 = provider_g1 or reg.get("provider")
            if reg.get("status", "").startswith("encerrada"):
                encerrada = True
    if encerrada or len(feitos) >= geracoes:
        return cid, "já completa/encerrada", len(feitos)

    prompt_modelo = PROMPTS[cond]
    for g in range(len(feitos) + 1, geracoes + 1):
        if PARAR.is_set():
            return cid, "pausada (teto de gasto)", g - 1
        prompt_texto = prompt_modelo.format(texto=texto)
        tent_conteudo = 0
        while True:
            # backoff para erros de infraestrutura
            atraso, tent_infra = 5, 0
            while True:
                try:
                    resp = chamar(modelo, prompt_texto)
                    break
                except (requests.RequestException, RuntimeError) as e:
                    tent_infra += 1
                    if tent_infra > 5:
                        registrar(caminho, cid, g, modelo, cond, resp=None,
                                  status="pausada-infra", erro=str(e)[:200])
                        return cid, f"pausada na G{g} (infra: {str(e)[:80]})", g - 1
                    time.sleep(atraso)
                    atraso = min(atraso * 2, 120)
            filtrado, removido = filtrar_moldura(resp["texto"])
            usd, brl = custo_por_chamada(modelo)  # estimativa; substituída se houver custo real
            if resp["custo_usd_provedor"] is not None:
                usd = float(resp["custo_usd_provedor"])
            somar_gasto(usd, brl)
            anomalia = None
            if resp["finish_reason"] == "length":
                anomalia = "saida-truncada"
            elif len(filtrado.split()) < 20:
                anomalia = "saida-vazia-ou-recusa"
            registrar(caminho, cid, g, modelo, cond, resp, filtrado, removido,
                      status="ok" if not anomalia else f"anomalia:{anomalia}",
                      usd=usd, brl=brl)
            if not anomalia:
                if g == 1 and provider_g1 is None:
                    provider_g1 = resp["provider"]
                elif provider_g1 and resp["provider"] != provider_g1:
                    registrar(caminho, cid, g, modelo, cond, resp=None,
                              status="encerrada-provedor-mudou",
                              erro=f"{provider_g1} -> {resp['provider']}")
                    return cid, f"encerrada na G{g} (provedor mudou)", g - 1
                texto = filtrado
                break
            tent_conteudo += 1
            if tent_conteudo >= 2:
                registrar(caminho, cid, g, modelo, cond, resp=None,
                          status=f"encerrada-{anomalia}")
                return cid, f"encerrada na G{g} ({anomalia})", g - 1
    return cid, "completa", geracoes


def registrar(caminho, cid, g, modelo, cond, resp, filtrado=None, removido=None,
              status="ok", erro=None, usd=0.0, brl=0.0):
    info = MODELOS[modelo]
    reg = {"ts": datetime.now(timezone.utc).isoformat(), "cadeia": cid,
           "geracao": g, "backend": info["backend"], "requested_model": modelo,
           "condicao": cond, "prompt_sha256": hash_prompt(cond),
           "params_enviados": info["params"], "params_documentados": info["documentado"],
           "status": status}
    if erro:
        reg["erro"] = erro
    if resp:
        reg.update({"response_model": resp["response_model"], "provider": resp["provider"],
                    "finish_reason": resp["finish_reason"], "tokens_in": resp["tokens_in"],
                    "tokens_out": resp["tokens_out"], "custo_usd": round(usd, 6),
                    "custo_brl": round(brl, 6), "saida_bruta": resp["texto"],
                    "saida_filtrada": filtrado, "filtro_removido": removido or []})
    with open(caminho, "a", encoding="utf-8") as f:
        f.write(json.dumps(reg, ensure_ascii=False) + "\n")


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pilot", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--arms", default="core,grafia")
    ap.add_argument("--models", default="")
    ap.add_argument("--max-gens", type=int, default=None)
    args = ap.parse_args()
    args.max_gens = args.max_gens or (5 if args.pilot else 20)
    if args.pilot:
        global DADOS
        DADOS = os.path.join(HERE, "dados", "piloto")

    cadeias = montar_cadeias(args)
    n_ch = len(cadeias) * args.max_gens
    # projeção: custo/chamada medido × nº de chamadas por cadeia
    proj_usd = proj_brl = 0.0
    for m, *_ in cadeias:
        u, b = custo_por_chamada(m)
        proj_usd += u * args.max_gens; proj_brl += b * args.max_gens
    print(f"cadeias: {len(cadeias)} | chamadas: {n_ch} | "
          f"projeção: US$ {proj_usd:.2f} + R$ {proj_brl:.2f} "
          f"(tetos: US$ {TETO_USD_TOTAL} / R$ {TETO_BRL_MARITACA})")
    if args.dry_run:
        for m, c, s, _, g in cadeias[:12]:
            print(f"  {m} | {c} | {s} | {g} gerações")
        if len(cadeias) > 12:
            print(f"  ... e mais {len(cadeias)-12}")
        return
    for var, back in (("OPENROUTER_API_KEY", "openrouter"), ("MARITACA_API_KEY", "maritaca")):
        if any(MODELOS[m]["backend"] == back for m, *_ in cadeias) and not os.environ.get(var):
            sys.exit(f"ERRO: {var} ausente do ambiente.")
    with ThreadPoolExecutor(max_workers=10) as ex:
        futs = [ex.submit(rodar_cadeia, m, c, s, t, g) for m, c, s, t, g in cadeias]
        for f in futs:
            cid, resultado, gs = f.result()
            print(f"[{gs:2d}] {resultado:40s} {cid}")
    gs = ler_gasto()
    print(f"\ngasto acumulado: US$ {gs['usd_total']:.2f} | Maritaca R$ {gs['brl_maritaca']:.2f}")
    if PARAR.is_set():
        print("ATENÇÃO: teto de gasto atingido; coleta interrompida de forma ordenada.")


if __name__ == "__main__":
    main()
