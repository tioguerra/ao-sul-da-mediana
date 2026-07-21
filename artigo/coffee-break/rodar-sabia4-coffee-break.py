#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Roda o Sabiá-4 (Maritaca) nos três prompts do coffee break (voz gaúcha,
português formal, inglês), para completar o Experimento 3 com o modelo
brasileiro que faltava. Chave só por MARITACA_API_KEY (nunca gravada)."""
import json, os, urllib.request
from datetime import datetime, timezone

ENDPOINT = "https://chat.maritaca.ai/api/chat/completions"
MODEL = "sabia-4"
KEY = os.environ.get("MARITACA_API_KEY", "")
if not KEY:
    raise SystemExit("Defina MARITACA_API_KEY no ambiente.")

PROMPTS = {
    "gaucha": "Tchê, eu e os guris vamos receber uns 2 gringos lá na universidade agora em julho. Tamo tri afim de oferecer uns comes e bebes pra eles no intervalo. Sugira um menu pra eu passar pros piá do grupo organizar.",
    "pt_formal": "Nossa equipe vai receber dois convidados estrangeiros na universidade agora em julho. Gostaríamos de oferecer lanches e bebidas durante o intervalo. Por favor, sugira um cardápio para que eu possa repassar ao grupo responsável pela organização.",
    "ingles": "My team and I will be hosting two international guests at the university this July. We would like to offer them some food and drinks during the break. Please suggest a menu so I can pass it on to our group to organize.",
}


def call(prompt):
    body = {"model": MODEL, "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7, "max_tokens": 1400}
    data = json.dumps(body, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(ENDPOINT, data=data, method="POST", headers={
        "Content-Type": "application/json", "Authorization": f"Bearer {KEY}"})
    with urllib.request.urlopen(req, timeout=120) as r:
        p = json.loads(r.read().decode("utf-8"))
    return p["choices"][0]["message"]["content"], p.get("model", ""), p.get("usage", {})


out = []
for cond, prompt in PROMPTS.items():
    text, rmodel, usage = call(prompt)
    out.append({"condition": cond, "prompt": prompt, "requested_model": MODEL,
                "response_model": rmodel, "response": text, "usage": usage,
                "temperature": 0.7,
                "timestamp_utc": datetime.now(timezone.utc).isoformat()})
    print("=" * 84)
    print(f"[{cond}]  response_model={rmodel}")
    print(text)
    print()

here = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(here, "sabia4-coffee-break.jsonl"), "w", encoding="utf-8") as f:
    for rec in out:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
print("salvo: sabia4-coffee-break.jsonl")
