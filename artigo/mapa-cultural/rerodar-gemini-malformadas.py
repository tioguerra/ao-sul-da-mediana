#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rerroda as chamadas do Gemini cuja resposta veio malformada (ex.: '10of'),
repetindo até obter uma escolha numérica pontuável. Recusas legítimas ficam
como estão. Chave só por OPENROUTER_API_KEY (nunca gravada)."""
import csv, json, os, re, time, urllib.request
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
AUD = os.path.join(HERE, "auditoria-llms-multicondicao.csv")
ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"
KEY = os.environ.get("OPENROUTER_API_KEY", "")
if not KEY:
    raise SystemExit("Defina OPENROUTER_API_KEY no ambiente.")

FAIXA = {"f118": (1, 10), "f120": (1, 10), "g006": (1, 4), "e018": (1, 3)}


def pontuar(item, texto):
    achados = [int(x) for x in re.findall(r"(?<!\d)(10|[1-9])(?!\d)", texto)]
    lo, hi = FAIXA[item]
    validos = [x for x in achados if lo <= x <= hi]
    return validos[0] if validos else None


def chamar(model, system, user):
    body = {"model": model,
            "messages": [{"role": "system", "content": system},
                         {"role": "user", "content": user}],
            "temperature": 0, "max_tokens": 60}
    data = json.dumps(body, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(ENDPOINT, data=data, method="POST", headers={
        "Content-Type": "application/json", "Authorization": f"Bearer {KEY}"})
    with urllib.request.urlopen(req, timeout=90) as r:
        p = json.loads(r.read().decode("utf-8"))
    return (p["choices"][0]["message"].get("content") or "").strip(), p.get("model", "")


rows = list(csv.DictReader(open(AUD)))
alvos = [r for r in rows if r["status"] == "invalid" and "gemini" in r["requested_model"].lower()
         and re.fullmatch(r"\s*\d+\s*of\s*", r["response_text"] or "")]
print(f"malformadas a rerodar: {len(alvos)}\n")

updates = {}
for r in alvos:
    item, model = r["item"], r["requested_model"]
    novo, score = None, None
    for tent in range(1, 4):
        txt, rmodel = chamar(model, r["system_prompt"], r["user_prompt"])
        s = pontuar(item, txt)
        print(f"[{r['condition']}/v{r['variant']}/{item}] tent {tent}: {txt!r} -> score {s}")
        if s is not None:
            novo, score = txt, s
            break
        time.sleep(1)
    if novo is None:
        print("  !! ainda sem número válido após 6 tentativas (mantém como está)")
        continue
    updates[(r["condition"], r["variant"], item)] = {
        "response_text": novo, "score": str(score), "status": "ok",
        "response_recorded_utc": datetime.now(timezone.utc).isoformat(),
        "note": "rerodada 21jul2026 (malformada original)"}

# grava updates de volta na auditoria
if updates:
    for r in rows:
        k = (r["condition"], r["variant"], r["item"])
        if k in updates:
            r["response_text"] = updates[k]["response_text"]
            r["score"] = updates[k]["score"]
            r["status"] = updates[k]["status"]
            r["error"] = ""
    with open(AUD, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=rows[0].keys())
        w.writeheader(); w.writerows(rows)
    print(f"\nauditoria atualizada: {len(updates)} respostas agora pontuáveis")
