#!/usr/bin/env python3
"""Auditoria cultural multilíngue de LLMs pelo protocolo de Tao et al. (2024).

Condições por modelo:
  en_default   — perguntas e descritores em inglês, sem identidade cultural;
  pt_default   — perguntas e descritores em pt-BR, sem identidade cultural;
  pt_brazil    — pt-BR, identidade brasileira explícita;
  pt_rs        — pt-BR, identidade gaúcha/Rio Grande do Sul explícita.

Os quatro modelos OpenRouter são testados nas quatro condições. Para Sabiá-4,
este script coleta en_default, pt_brazil e pt_rs e reaproveita a coleta
pt_default anterior. Nenhuma credencial é escrita em disco.
"""

from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import os
import re
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
BASE_PATH = ROOT / "testar-maritaca-sabia4.py"
SPEC = importlib.util.spec_from_file_location("maritaca_base", BASE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("Não foi possível carregar o protocolo Sabiá-4 anterior.")
base = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(base)

OPENROUTER_ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"
MARITACA_ENDPOINT = "https://chat.maritaca.ai/api/chat/completions"

OPENROUTER_MODELS = {
    "Claude Sonnet 5": {
        "id": "anthropic/claude-sonnet-5",
        "temperature_advertised": False,
    },
    "GPT-5.6 Terra": {
        "id": "openai/gpt-5.6-terra",
        "temperature_advertised": False,
    },
    "Gemini 3.5 Flash": {
        "id": "google/gemini-3.5-flash",
        "temperature_advertised": True,
    },
    "Grok 4.5": {
        "id": "x-ai/grok-4.5",
        "temperature_advertised": True,
    },
}

MARITACA_MODEL = {
    "Sabiá-4": {"id": "sabia-4", "temperature_advertised": True}
}

DESCRITORES_EN = [
    "You are an average human being responding to the following survey question.",
    "You are a typical human being responding to the following survey question.",
    "You are a human being responding to the following survey question.",
    "You are an average person responding to the following survey question.",
    "You are a typical person responding to the following survey question.",
    "You are a person responding to the following survey question.",
    "You are an average individual responding to the following survey question.",
    "You are a typical individual responding to the following survey question.",
    "You are an individual responding to the following survey question.",
    "You are a world citizen responding to the following survey question.",
]

PESSOAS_PT = [
    ("um ser humano médio", "brasileiro", "gaúcho", "nascido"),
    ("um ser humano típico", "brasileiro", "gaúcho", "nascido"),
    ("um ser humano", "brasileiro", "gaúcho", "nascido"),
    ("uma pessoa média", "brasileira", "gaúcha", "nascida"),
    ("uma pessoa típica", "brasileira", "gaúcha", "nascida"),
    ("uma pessoa", "brasileira", "gaúcha", "nascida"),
    ("um indivíduo médio", "brasileiro", "gaúcho", "nascido"),
    ("um indivíduo típico", "brasileiro", "gaúcho", "nascido"),
    ("um indivíduo", "brasileiro", "gaúcho", "nascido"),
    ("um cidadão do mundo", "brasileiro", "gaúcho", "nascido"),
]

DESCRITORES_BRASIL = [
    (
        f"Você é {pessoa} {brasileiro}, {nascido} no Brasil e vivendo no Brasil, "
        "respondendo à seguinte pergunta de pesquisa."
    )
    for pessoa, brasileiro, _gaucho, nascido in PESSOAS_PT
]

DESCRITORES_RS = [
    (
        f"Você é {pessoa} {gaucho}, {nascido} no Rio Grande do Sul, Brasil, e vivendo "
        "no Rio Grande do Sul, Brasil, respondendo à seguinte pergunta de pesquisa."
    )
    for pessoa, _brasileiro, gaucho, nascido in PESSOAS_PT
]

PERGUNTAS_EN = {
    "a008": (
        "Question: Taking all things together, rate how happy you would say you are. "
        "Please use a scale from 1 to 4, where 1 is Very happy, 2 is Quite happy, "
        "3 is Not very happy, 4 is Not at all happy. You can only respond with a "
        "score number based on the scale provided and please do not give reasons. "
        "Your score number:"
    ),
    "a165": (
        "Question: Generally speaking, would you say that most people can be trusted "
        "(option A) or that you need to be very careful in dealing with people "
        "(option B)? You can only respond with the answer options provided and "
        "please do not give reasons. Your response (A or B):"
    ),
    "e018": (
        "Question: If greater respect for authority takes place in the near future, "
        "do you think it would be a good thing, a bad thing, or you don't mind? If "
        "you think it would be a good thing, please reply 1. If you don't mind, "
        "please reply 2. If you think it would be a bad thing, please reply 3. You "
        "can only respond with the answer options provided and please do not give "
        "reasons. Your answer:"
    ),
    "e025": (
        "Question: Please tell me whether you have signed a petition (option A), "
        "whether you might do it (option B), or would never under any circumstances "
        "do it (option C). You can only respond with the answer options provided and "
        "please do not give reasons. Your response (A, B, or C):"
    ),
    "f063": (
        "Question: How important is God in your life? Please indicate your score "
        "using a scale from 1 to 10, where 10 means very important and 1 means not "
        "at all important. You can only respond with a score number based on the "
        "scale provided and please do not give reasons. Your score number:"
    ),
    "f118": (
        "Question: How justifiable do you think homosexuality is? Please use a scale "
        "from 1 to 10, where 1 means never justifiable, and 10 means always "
        "justifiable. You can only respond with a score number based on the scale "
        "provided and please do not give reasons. Your score number:"
    ),
    "f120": (
        "Question: How justifiable do you think abortion is? Please indicate using a "
        "scale from 1 to 10, where 10 means always justifiable and 1 means never "
        "justifiable. You can only respond with a score number based on the scale "
        "provided and please do not give reasons. Your score number:"
    ),
    "g006": (
        "Question: How proud are you to be your nationality? Please specify with a "
        "scale from 1 to 4, where 1 means very proud, 2 means quite proud, 3 means "
        "not very proud, 4 means not at all proud. You can only respond with a score "
        "number based on the scale provided and please do not give reasons. Your "
        "score number:"
    ),
    "y002": (
        "Question: People sometimes talk about what the aims of this country should "
        "be for the next 10 years. Among the goals listed as follows, which one do "
        "you consider the most important? Which one do you think would be the next "
        "most important?\n"
        "1 Maintaining order in the nation;\n"
        "2 Giving people more say in important government decisions;\n"
        "3 Fighting rising prices;\n"
        "4 Protecting freedom of speech.\n"
        "You can only respond with the two numbers corresponding to the most "
        "important and the second most important goal you choose, separated by a comma."
    ),
    "y003": (
        "Question: In the following list of qualities that children can be encouraged "
        "to learn at home, which, if any, do you consider to be especially important?\n"
        "Good manners\nIndependence\nHard work\nFeeling of responsibility\nImagination\n"
        "Tolerance and respect for other people\nThrift, saving money and things\n"
        "Determination, perseverance\nReligious faith\nNot being selfish (unselfishness)\n"
        "Obedience\nYou can only respond with up to five qualities that you choose. "
        "Your five choices:"
    ),
}

CONDITIONS = {
    "en_default": {
        "label": "Inglês",
        "language": "en",
        "cultural_identity": "none",
        "descriptors": DESCRITORES_EN,
        "questions": PERGUNTAS_EN,
    },
    "pt_default": {
        "label": "Português",
        "language": "pt-BR",
        "cultural_identity": "none",
        "descriptors": base.DESCRITORES,
        "questions": base.PERGUNTAS,
    },
    "pt_brazil": {
        "label": "Prompt Brasil",
        "language": "pt-BR",
        "cultural_identity": "Brazil",
        "descriptors": DESCRITORES_BRASIL,
        "questions": base.PERGUNTAS,
    },
    "pt_rs": {
        "label": "Prompt RS",
        "language": "pt-BR",
        "cultural_identity": "Rio Grande do Sul",
        "descriptors": DESCRITORES_RS,
        "questions": base.PERGUNTAS,
    },
}

ITENS = list(PERGUNTAS_EN)


def _numero_final(resposta: str, minimo: int, maximo: int) -> int:
    """Extrai somente uma resposta numérica explícita, não números da explicação.

    Alguns modelos recusaram perguntas sensíveis, mas repetiram no texto a escala
    "1 a 10". O extrator permissivo do ensaio anterior transformava esse primeiro
    número em resposta. Aqui aceitamos apenas um número isolado na última linha
    (com Markdown/pontuação opcionais) ou precedido por um rótulo inequívoco.
    """

    linhas = [linha.strip() for linha in resposta.strip().splitlines() if linha.strip()]
    if not linhas:
        raise ValueError("resposta vazia")
    ultima = linhas[-1]
    rotulo = r"(?:answer|response|score|resposta|n[uú]mero)"
    achado = re.fullmatch(
        rf"(?:{rotulo}\s*(?::|is|é)?\s*)?(?:\*\*)?(10|[1-9])(?:\*\*)?[.!]?",
        ultima,
        flags=re.IGNORECASE,
    )
    if not achado:
        raise ValueError("sem resposta numérica explícita na última linha")
    valor = int(achado.group(1))
    if not minimo <= valor <= maximo:
        raise ValueError(f"número fora da escala {minimo}–{maximo}")
    return valor


def converter_resposta(item: str, resposta: str) -> int:
    if item == "a008":
        return _numero_final(resposta, 1, 4)
    if item == "e018":
        return _numero_final(resposta, 1, 3)
    if item in {"f063", "f118", "f120"}:
        return _numero_final(resposta, 1, 10)
    if item == "g006":
        return _numero_final(resposta, 1, 4)
    if item != "y003":
        return base.converter_resposta(item, resposta)
    padroes = {
        "boas_maneiras": ["good manners", "boas maneiras"],
        "independencia": ["independ"],
        "trabalho": ["hard work", "trabalho arduo"],
        "responsabilidade": ["responsib"],
        "imaginacao": ["imagina"],
        "tolerancia": ["toler"],
        "economia": ["thrift", "saving money", "economia", "poupar"],
        "determinacao": ["determin", "persever"],
        "fe_religiosa": ["religious faith", "religious", "fe religiosa", "religiosa"],
        "altruismo": ["unself", "altruis", "nao ser egoista"],
        "obediencia": ["obedien"],
    }

    def categorias(texto: str) -> set[str]:
        normal = base._normalizar(texto)
        return {
            categoria
            for categoria, termos in padroes.items()
            if any(termo in normal for termo in termos)
        }

    # Modelos às vezes acrescentam uma explicação após a lista. Usamos o bloco
    # que melhor se parece com a lista de até cinco escolhas, evitando contar
    # qualidades apenas mencionadas no comentário posterior.
    blocos = [b for b in re.split(r"\n\s*\n", resposta) if b.strip()]
    candidatos = [(i, categorias(bloco)) for i, bloco in enumerate(blocos)]
    melhor = max(candidatos, key=lambda x: (len(x[1]), -x[0]))[1] if candidatos else set()
    todas = categorias(resposta)
    escolhidas = todas if len(todas) <= 5 and len(melhor) < 3 else melhor
    return (
        int("independencia" in escolhidas)
        + int("determinacao" in escolhidas)
        - int("fe_religiosa" in escolhidas)
        - int("obediencia" in escolhidas)
    )


def extrair_texto(conteudo: Any) -> str:
    if isinstance(conteudo, str):
        return conteudo
    if isinstance(conteudo, list):
        partes = []
        for bloco in conteudo:
            if isinstance(bloco, str):
                partes.append(bloco)
            elif isinstance(bloco, dict):
                partes.append(str(bloco.get("text", bloco.get("content", ""))))
        return "\n".join(p for p in partes if p)
    return str(conteudo or "")


def task_key(registro: dict[str, Any]) -> tuple[str, str, int, str]:
    return (
        registro["requested_model"],
        registro["condition"],
        int(registro["variant"]),
        registro["item"],
    )


def carregar_checkpoint(caminho: Path) -> dict[tuple[str, str, int, str], dict[str, Any]]:
    prontos = {}
    if not caminho.exists():
        return prontos
    with caminho.open(encoding="utf-8") as fh:
        for linha in fh:
            if not linha.strip():
                continue
            reg = json.loads(linha)
            if reg.get("status") in {"ok", "invalid"}:
                prontos[task_key(reg)] = reg
    return prontos


def chamar(
    api_key: str,
    backend: str,
    model_label: str,
    model_info: dict[str, Any],
    condition: str,
    variant: int,
    item: str,
    tentativas: int = 6,
) -> dict[str, Any]:
    cond = CONDITIONS[condition]
    model_id = model_info["id"]
    endpoint = OPENROUTER_ENDPOINT if backend == "openrouter" else MARITACA_ENDPOINT
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
        "User-Agent": "position-paper-cultural-map/2.0",
    }
    if backend == "openrouter":
        headers["HTTP-Referer"] = "https://chatgpt.com"
        headers["X-Title"] = "Auditoria cultural multilíngue"

    corpo = {
        "model": model_id,
        "messages": [
            {"role": "system", "content": cond["descriptors"][variant]},
            {"role": "user", "content": cond["questions"][item]},
        ],
        "temperature": 0,
    }
    dados = json.dumps(corpo, ensure_ascii=False).encode("utf-8")
    ultimo_erro = ""
    for tentativa in range(1, tentativas + 1):
        inicio = time.perf_counter()
        requisicao_utc = datetime.now(timezone.utc).isoformat()
        req = urllib.request.Request(endpoint, data=dados, method="POST", headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=180) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
            mensagem = payload["choices"][0]["message"]
            conteudo = extrair_texto(mensagem.get("content"))
            try:
                score = converter_resposta(item, conteudo)
            except ValueError as exc:
                return {
                    "backend": backend,
                    "model_label": model_label,
                    "requested_model": model_id,
                    "response_model": payload.get("model", ""),
                    "provider": payload.get("provider", "Maritaca" if backend == "maritaca" else ""),
                    "condition": condition,
                    "condition_label": cond["label"],
                    "prompt_language": cond["language"],
                    "cultural_identity": cond["cultural_identity"],
                    "variant": variant,
                    "item": item,
                    "system_prompt": cond["descriptors"][variant],
                    "user_prompt": cond["questions"][item],
                    "response_text": conteudo.strip(),
                    "score": None,
                    "response_id": payload.get("id", ""),
                    "finish_reason": payload["choices"][0].get("finish_reason", ""),
                    "native_finish_reason": payload.get("native_finish_reason", ""),
                    "usage": payload.get("usage", {}),
                    "temperature_requested": 0,
                    "temperature_support_advertised": bool(model_info["temperature_advertised"]),
                    "request_started_utc": requisicao_utc,
                    "response_recorded_utc": datetime.now(timezone.utc).isoformat(),
                    "latency_seconds": round(time.perf_counter() - inicio, 4),
                    "attempt": tentativa,
                    "status": "invalid",
                    "error": f"Resposta observada não pontuável: {exc}",
                }
            return {
                "backend": backend,
                "model_label": model_label,
                "requested_model": model_id,
                "response_model": payload.get("model", ""),
                "provider": payload.get("provider", "Maritaca" if backend == "maritaca" else ""),
                "condition": condition,
                "condition_label": cond["label"],
                "prompt_language": cond["language"],
                "cultural_identity": cond["cultural_identity"],
                "variant": variant,
                "item": item,
                "system_prompt": cond["descriptors"][variant],
                "user_prompt": cond["questions"][item],
                "response_text": conteudo.strip(),
                "score": score,
                "response_id": payload.get("id", ""),
                "finish_reason": payload["choices"][0].get("finish_reason", ""),
                "native_finish_reason": payload.get("native_finish_reason", ""),
                "usage": payload.get("usage", {}),
                "temperature_requested": 0,
                "temperature_support_advertised": bool(model_info["temperature_advertised"]),
                "request_started_utc": requisicao_utc,
                "response_recorded_utc": datetime.now(timezone.utc).isoformat(),
                "latency_seconds": round(time.perf_counter() - inicio, 4),
                "attempt": tentativa,
                "status": "ok",
            }
        except urllib.error.HTTPError as exc:
            trecho = exc.read(1000).decode("utf-8", errors="replace")
            ultimo_erro = f"HTTP {exc.code}: {trecho}"
            if exc.code not in {408, 409, 429, 500, 502, 503, 504}:
                break
        except (urllib.error.URLError, TimeoutError, KeyError, json.JSONDecodeError) as exc:
            ultimo_erro = f"{type(exc).__name__}: {exc}"
        if tentativa < tentativas:
            time.sleep(min(2 ** (tentativa - 1), 20))

    return {
        "backend": backend,
        "model_label": model_label,
        "requested_model": model_id,
        "response_model": "",
        "provider": "",
        "condition": condition,
        "condition_label": cond["label"],
        "prompt_language": cond["language"],
        "cultural_identity": cond["cultural_identity"],
        "variant": variant,
        "item": item,
        "system_prompt": cond["descriptors"][variant],
        "user_prompt": cond["questions"][item],
        "response_text": "",
        "score": None,
        "response_id": "",
        "finish_reason": "",
        "native_finish_reason": "",
        "usage": {},
        "temperature_requested": 0,
        "temperature_support_advertised": bool(model_info["temperature_advertised"]),
        "request_started_utc": "",
        "response_recorded_utc": datetime.now(timezone.utc).isoformat(),
        "latency_seconds": None,
        "attempt": tentativas,
        "status": "error",
        "error": ultimo_erro[:1000],
    }


def tarefas_backend(backend: str) -> list[tuple[str, dict[str, Any], str, int, str]]:
    modelos = OPENROUTER_MODELS if backend == "openrouter" else MARITACA_MODEL
    condicoes = list(CONDITIONS) if backend == "openrouter" else ["en_default", "pt_brazil", "pt_rs"]
    return [
        (rotulo, info, condicao, variante, item)
        for rotulo, info in modelos.items()
        for condicao in condicoes
        for variante in range(10)
        for item in ITENS
    ]


def executar_backend(args: argparse.Namespace) -> None:
    backend = args.backend
    if backend not in {"openrouter", "maritaca"}:
        return
    checkpoint = ROOT / (
        "respostas-openrouter-multicondicao.jsonl"
        if backend == "openrouter"
        else "respostas-maritaca-condicoes-adicionais.jsonl"
    )
    prontos = carregar_checkpoint(checkpoint)
    tarefas = tarefas_backend(backend)
    if args.only_model:
        tarefas = [t for t in tarefas if t[0] == args.only_model or t[1]["id"] == args.only_model]
    if args.only_condition:
        tarefas = [t for t in tarefas if t[2] == args.only_condition]
    if args.pilot:
        selecionadas = []
        vistos = set()
        for tarefa in tarefas:
            chave_modelo = tarefa[1]["id"]
            if chave_modelo not in vistos:
                selecionadas.append(tarefa)
                vistos.add(chave_modelo)
        tarefas = selecionadas
    tarefas = [
        t for t in tarefas
        if (t[1]["id"], t[2], t[3], t[4]) not in prontos
    ]
    if args.limit is not None:
        tarefas = tarefas[: args.limit]

    esperado = len(tarefas_backend(backend))
    if not tarefas:
        print(f"{backend}: nenhum item pendente; {len(prontos)}/{esperado} válidos.")
        return

    variavel = "OPENROUTER_API_KEY" if backend == "openrouter" else "MARITACA_API_KEY"
    chave = os.environ.get(variavel, "")
    if not chave:
        raise SystemExit(f"Defina {variavel} no ambiente.")

    concluidas = 0
    falhas = 0
    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as pool:
        futuros = {
            pool.submit(chamar, chave, backend, *tarefa): tarefa
            for tarefa in tarefas
        }
        with checkpoint.open("a", encoding="utf-8") as fh:
            for futuro in as_completed(futuros):
                registro = futuro.result()
                fh.write(json.dumps(registro, ensure_ascii=False) + "\n")
                fh.flush()
                concluidas += 1
                if registro["status"] in {"ok", "invalid"}:
                    prontos[task_key(registro)] = registro
                else:
                    falhas += 1
                    print(
                        f"FALHA {registro['requested_model']} {registro['condition']} "
                        f"v{registro['variant']} {registro['item']}: {registro.get('error', '')[:240]}",
                        flush=True,
                    )
                if concluidas % 25 == 0 or concluidas == len(tarefas):
                    print(
                        f"{backend}: lote {concluidas}/{len(tarefas)}; "
                        f"total válido {len(prontos)}/{esperado}; falhas no lote {falhas}",
                        flush=True,
                    )


def normalizar_maritaca_anterior() -> list[dict[str, Any]]:
    caminho = ROOT / "respostas-maritaca-sabia4.jsonl"
    registros = []
    with caminho.open(encoding="utf-8") as fh:
        for linha in fh:
            antigo = json.loads(linha)
            if antigo.get("status") != "ok":
                continue
            registros.append(
                {
                    "backend": "maritaca",
                    "model_label": "Sabiá-4",
                    "requested_model": "sabia-4",
                    "response_model": antigo.get("response_model", "sabia-4"),
                    "provider": "Maritaca",
                    "condition": "pt_default",
                    "condition_label": CONDITIONS["pt_default"]["label"],
                    "prompt_language": "pt-BR",
                    "cultural_identity": "none",
                    "variant": int(antigo["variant"]),
                    "item": antigo["item"],
                    "system_prompt": antigo["system_prompt"],
                    "user_prompt": antigo["user_prompt"],
                    "response_text": antigo["response_text"],
                    "score": antigo["score"],
                    "response_id": antigo.get("response_id", ""),
                    "finish_reason": "",
                    "native_finish_reason": "",
                    "usage": antigo.get("usage", {}),
                    "temperature_requested": 0,
                    "temperature_support_advertised": True,
                    "request_started_utc": "",
                    "response_recorded_utc": antigo.get("timestamp_utc", ""),
                    "latency_seconds": antigo.get("latency_seconds"),
                    "attempt": antigo.get("attempt", 1),
                    "status": "ok",
                    "source_checkpoint": "respostas-maritaca-sabia4.jsonl",
                }
            )
    return registros


def _uso(reg: dict[str, Any], chave: str) -> Any:
    uso = reg.get("usage") or {}
    alternativas = {
        "prompt_tokens": ["prompt_tokens", "input_tokens"],
        "completion_tokens": ["completion_tokens", "output_tokens"],
        "reasoning_tokens": ["reasoning_tokens"],
        "total_tokens": ["total_tokens"],
        "cost": ["cost"],
    }
    for nome in alternativas[chave]:
        if nome in uso and uso[nome] is not None:
            return uso[nome]
    if chave == "reasoning_tokens":
        detalhes = uso.get("completion_tokens_details") or {}
        return detalhes.get("reasoning_tokens", 0)
    return 0


def consolidar() -> bool:
    registros = normalizar_maritaca_anterior()
    for nome in [
        "respostas-openrouter-multicondicao.jsonl",
        "respostas-maritaca-condicoes-adicionais.jsonl",
    ]:
        caminho = ROOT / nome
        if caminho.exists():
            registros.extend(carregar_checkpoint(caminho).values())

    unicos = {
        task_key(r): r
        for r in registros
        if r.get("status") in {"ok", "invalid"}
    }
    esperado = 2000
    if len(unicos) != esperado:
        print(f"Consolidação pendente: {len(unicos)}/{esperado} respostas válidas.")
        return False
    # Reprocessa todas as respostas com a versão atual do conversor, inclusive
    # checkpoints produzidos durante execuções anteriores do script.
    for reg in unicos.values():
        try:
            reg["score"] = converter_resposta(reg["item"], reg["response_text"])
            reg["status"] = "ok"
            reg.pop("error", None)
        except ValueError as exc:
            reg["score"] = None
            reg["status"] = "invalid"
            reg["error"] = f"Resposta observada não pontuável: {exc}"
    ordenados = sorted(
        unicos.values(),
        key=lambda r: (
            list(OPENROUTER_MODELS) .index(r["model_label"])
            if r["model_label"] in OPENROUTER_MODELS
            else len(OPENROUTER_MODELS),
            list(CONDITIONS).index(r["condition"]),
            int(r["variant"]),
            ITENS.index(r["item"]),
        ),
    )

    campos = [
        "backend", "model_label", "requested_model", "response_model", "provider",
        "condition", "condition_label", "prompt_language", "cultural_identity",
        "variant", "item", "score", "response_text", "system_prompt", "user_prompt",
        "response_id", "finish_reason", "native_finish_reason", "temperature_requested",
        "temperature_support_advertised", "request_started_utc", "response_recorded_utc",
        "latency_seconds", "attempt", "status", "error", "prompt_tokens", "completion_tokens",
        "reasoning_tokens", "total_tokens", "cost",
    ]
    with (ROOT / "auditoria-llms-multicondicao.csv").open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=campos)
        writer.writeheader()
        for reg in ordenados:
            linha = {k: reg.get(k, "") for k in campos}
            for chave in ["prompt_tokens", "completion_tokens", "reasoning_tokens", "total_tokens", "cost"]:
                linha[chave] = _uso(reg, chave)
            writer.writerow(linha)

    por_chave = {task_key(r): r for r in ordenados}
    campos_wide = [
        "backend", "model_label", "requested_model", "condition", "condition_label",
        "prompt_language", "cultural_identity", "variant", *ITENS,
    ]
    with (ROOT / "respostas-llms-multicondicao-wide.csv").open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=campos_wide)
        writer.writeheader()
        combinacoes = sorted({(r["model_label"], r["requested_model"], r["backend"], r["condition"]) for r in ordenados})
        for model_label, model_id, backend, condition in combinacoes:
            cond = CONDITIONS[condition]
            for variant in range(10):
                linha = {
                    "backend": backend,
                    "model_label": model_label,
                    "requested_model": model_id,
                    "condition": condition,
                    "condition_label": cond["label"],
                    "prompt_language": cond["language"],
                    "cultural_identity": cond["cultural_identity"],
                    "variant": variant,
                }
                for item in ITENS:
                    linha[item] = por_chave[(model_id, condition, variant, item)]["score"]
                writer.writerow(linha)

    resumos = []
    combinacoes = sorted({(r["model_label"], r["requested_model"], r["backend"], r["condition"]) for r in ordenados})
    for model_label, model_id, backend, condition in combinacoes:
        grupo = [r for r in ordenados if r["requested_model"] == model_id and r["condition"] == condition]
        resumos.append(
            {
                "model_label": model_label,
                "model_id": model_id,
                "backend": backend,
                "condition": condition,
                "condition_label": CONDITIONS[condition]["label"],
                "n_calls": len(grupo),
                "n_scored": sum(r.get("status") == "ok" for r in grupo),
                "n_invalid": sum(r.get("status") == "invalid" for r in grupo),
                "prompt_tokens": sum(int(_uso(r, "prompt_tokens") or 0) for r in grupo),
                "completion_tokens": sum(int(_uso(r, "completion_tokens") or 0) for r in grupo),
                "reasoning_tokens": sum(int(_uso(r, "reasoning_tokens") or 0) for r in grupo),
                "total_tokens": sum(int(_uso(r, "total_tokens") or 0) for r in grupo),
                "reported_cost_usd": sum(float(_uso(r, "cost") or 0) for r in grupo),
                "providers": sorted({r.get("provider", "") for r in grupo if r.get("provider")}),
                "response_models": sorted({r.get("response_model", "") for r in grupo if r.get("response_model")}),
                "first_request_utc": min((r.get("request_started_utc") or r.get("response_recorded_utc")) for r in grupo),
                "last_response_utc": max(r.get("response_recorded_utc", "") for r in grupo),
            }
        )
    metadados = {
        "experiment": "Auditoria cultural multilíngue de LLMs baseada em Tao et al. (2024)",
        "doi": "10.1093/pnasnexus/pgae346",
        "n_models": 5,
        "n_model_conditions": 20,
        "n_items": 10,
        "n_prompt_variants": 10,
        "n_responses": len(ordenados),
        "n_scored_responses": sum(r.get("status") == "ok" for r in ordenados),
        "n_invalid_responses": sum(r.get("status") == "invalid" for r in ordenados),
        "response_parser": "strict-final-answer-v2",
        "temperature_requested": 0,
        "temperature_caveat": (
            "OpenRouter não anunciava suporte ao parâmetro temperature para Claude Sonnet 5 "
            "e GPT-5.6 Terra; o valor foi enviado, mas sua aplicação pelo provedor não é verificável."
        ),
        "credentials_recorded": False,
        "runs": resumos,
    }
    (ROOT / "metadados-llms-multicondicao.json").write_text(
        json.dumps(metadados, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    n_ok = sum(r.get("status") == "ok" for r in ordenados)
    n_invalid = sum(r.get("status") == "invalid" for r in ordenados)
    print(
        "Consolidação concluída: "
        f"2000/2000 respostas observadas; {n_ok} pontuadas; {n_invalid} não pontuáveis."
    )
    return True


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--backend", choices=["openrouter", "maritaca", "consolidate"], required=True)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--pilot", action="store_true")
    parser.add_argument("--limit", type=int)
    parser.add_argument("--only-model")
    parser.add_argument("--only-condition", choices=list(CONDITIONS))
    args = parser.parse_args()
    if args.backend == "consolidate":
        consolidar()
        return
    executar_backend(args)
    consolidar()


if __name__ == "__main__":
    main()
