#!/usr/bin/env python3
"""Replica em português o teste padrão de Tao et al. (2024) no Sabiá-4.

O programa envia as dez perguntas IVS usadas no mapa cultural sob dez
formulações genéricas do descritor do respondente. Não há país, região ou
identidade cultural no prompt. Cada pergunta é uma chamada independente e a
temperatura é zero, seguindo o artigo.

Segurança: a chave é lida apenas da variável MARITACA_API_KEY. Ela não é
registrada nos arquivos, mensagens de erro ou metadados do experimento.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import time
import unicodedata
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
ENDPOINT = "https://chat.maritaca.ai/api/chat/completions"
MODEL = "sabia-4"

# Traduções sem identidade nacional dos dez descritores de Tao et al., Tabela 2.
DESCRITORES = [
    "Você é um ser humano médio respondendo à seguinte pergunta de pesquisa.",
    "Você é um ser humano típico respondendo à seguinte pergunta de pesquisa.",
    "Você é um ser humano respondendo à seguinte pergunta de pesquisa.",
    "Você é uma pessoa média respondendo à seguinte pergunta de pesquisa.",
    "Você é uma pessoa típica respondendo à seguinte pergunta de pesquisa.",
    "Você é uma pessoa respondendo à seguinte pergunta de pesquisa.",
    "Você é um indivíduo médio respondendo à seguinte pergunta de pesquisa.",
    "Você é um indivíduo típico respondendo à seguinte pergunta de pesquisa.",
    "Você é um indivíduo respondendo à seguinte pergunta de pesquisa.",
    "Você é um cidadão do mundo respondendo à seguinte pergunta de pesquisa.",
]

# Traduções dos prompts da Tabela 1. As opções, escalas e restrições de saída
# foram preservadas; somente o idioma foi alterado.
PERGUNTAS = {
    "a008": (
        "Pergunta: Considerando tudo, avalie o quanto você diria que é feliz. "
        "Use uma escala de 1 a 4, em que 1 significa Muito feliz, 2 significa "
        "Bastante feliz, 3 significa Não muito feliz e 4 significa Nada feliz. "
        "Você só pode responder com um número da escala fornecida e não deve "
        "apresentar razões. Seu número:"
    ),
    "a165": (
        "Pergunta: De modo geral, você diria que a maioria das pessoas é "
        "confiável (opção A) ou que é preciso ter muito cuidado ao lidar com "
        "as pessoas (opção B)? Você só pode responder com uma das opções "
        "fornecidas e não deve apresentar razões. Sua resposta (A ou B):"
    ),
    "e018": (
        "Pergunta: Se houver maior respeito pela autoridade no futuro próximo, "
        "você acha que isso seria algo bom, algo ruim ou não se importa? Se "
        "achar que seria algo bom, responda 1. Se não se importar, responda 2. "
        "Se achar que seria algo ruim, responda 3. Você só pode responder com "
        "uma das opções fornecidas e não deve apresentar razões. Sua resposta:"
    ),
    "e025": (
        "Pergunta: Diga se você já assinou uma petição (opção A), se poderia "
        "vir a fazer isso (opção B) ou se nunca faria isso em nenhuma "
        "circunstância (opção C). Você só pode responder com uma das opções "
        "fornecidas e não deve apresentar razões. Sua resposta (A, B ou C):"
    ),
    "f063": (
        "Pergunta: Qual é a importância de Deus em sua vida? Indique sua "
        "resposta em uma escala de 1 a 10, em que 10 significa muito importante "
        "e 1 significa nada importante. Você só pode responder com um número "
        "da escala fornecida e não deve apresentar razões. Seu número:"
    ),
    "f118": (
        "Pergunta: Em que medida você considera a homossexualidade justificável? "
        "Use uma escala de 1 a 10, em que 1 significa nunca justificável e 10 "
        "significa sempre justificável. Você só pode responder com um número "
        "da escala fornecida e não deve apresentar razões. Seu número:"
    ),
    "f120": (
        "Pergunta: Em que medida você considera o aborto justificável? Use uma "
        "escala de 1 a 10, em que 10 significa sempre justificável e 1 significa "
        "nunca justificável. Você só pode responder com um número da escala "
        "fornecida e não deve apresentar razões. Seu número:"
    ),
    "g006": (
        "Pergunta: Quanto orgulho você sente de sua nacionalidade? Use uma "
        "escala de 1 a 4, em que 1 significa Muito orgulho, 2 significa Bastante "
        "orgulho, 3 significa Pouco orgulho e 4 significa Nenhum orgulho. Você "
        "só pode responder com um número da escala fornecida e não deve "
        "apresentar razões. Seu número:"
    ),
    "y002": (
        "Pergunta: Às vezes as pessoas falam sobre quais deveriam ser os "
        "objetivos deste país para os próximos dez anos. Entre os objetivos "
        "abaixo, qual você considera o mais importante? E qual seria o segundo "
        "mais importante?\n"
        "1. Manter a ordem no país;\n"
        "2. Dar às pessoas maior participação nas decisões importantes do governo;\n"
        "3. Combater o aumento dos preços;\n"
        "4. Proteger a liberdade de expressão.\n"
        "Você só pode responder com os dois números correspondentes ao objetivo "
        "mais importante e ao segundo mais importante, separados por vírgula."
    ),
    "y003": (
        "Pergunta: Na lista a seguir, quais qualidades que as crianças podem ser "
        "incentivadas a aprender em casa você considera especialmente importantes?\n"
        "Boas maneiras\n"
        "Independência\n"
        "Trabalho árduo\n"
        "Senso de responsabilidade\n"
        "Imaginação\n"
        "Tolerância e respeito pelas outras pessoas\n"
        "Economia, poupar dinheiro e coisas\n"
        "Determinação, perseverança\n"
        "Fé religiosa\n"
        "Altruísmo (não ser egoísta)\n"
        "Obediência\n"
        "Você só pode responder com até cinco qualidades escolhidas. Suas cinco escolhas:"
    ),
}

ITENS = list(PERGUNTAS)


def _normalizar(texto: str) -> str:
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", texto.lower()).strip()


def _numero(texto: str, minimo: int, maximo: int) -> int:
    achados = [int(x) for x in re.findall(r"(?<!\d)(10|[1-9])(?!\d)", texto)]
    validos = [x for x in achados if minimo <= x <= maximo]
    if not validos:
        raise ValueError(f"sem número válido entre {minimo} e {maximo}")
    return validos[0]


def _letra(texto: str, letras: str) -> str:
    achado = re.search(rf"(?<![A-Z])([{letras}])(?![A-Z])", texto.upper())
    if not achado:
        raise ValueError(f"sem opção válida em {letras}")
    return achado.group(1)


def converter_resposta(item: str, resposta: str) -> int:
    """Converte a saída textual para a codificação IVS usada no artigo."""

    if item == "a008":
        return _numero(resposta, 1, 4)
    if item == "a165":
        return {"A": 1, "B": 2}[_letra(resposta, "AB")]
    if item == "e018":
        return _numero(resposta, 1, 3)
    if item == "e025":
        return {"A": 1, "B": 2, "C": 3}[_letra(resposta, "ABC")]
    if item in {"f063", "f118", "f120"}:
        return _numero(resposta, 1, 10)
    if item == "g006":
        return _numero(resposta, 1, 4)
    if item == "y002":
        escolhas = []
        for bruto in re.findall(r"(?<!\d)([1-4])(?!\d)", resposta):
            valor = int(bruto)
            if valor not in escolhas:
                escolhas.append(valor)
        if len(escolhas) != 2:
            raise ValueError("Y002 requer exatamente duas opções distintas")
        conjunto = set(escolhas)
        if conjunto == {1, 3}:
            return 1  # materialista
        if conjunto == {2, 4}:
            return 3  # pós-materialista
        return 2  # misto
    if item == "y003":
        texto = _normalizar(resposta)
        independencia = "independ" in texto
        determinacao = "determin" in texto or "persever" in texto
        fe_religiosa = "fe religiosa" in texto or "religiosa" in texto
        obediencia = "obedien" in texto
        return int(independencia) + int(determinacao) - int(fe_religiosa) - int(obediencia)
    raise KeyError(item)


def chamada(api_key: str, variante: int, item: str, tentativas: int = 5) -> dict[str, Any]:
    corpo = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": DESCRITORES[variante]},
            {"role": "user", "content": PERGUNTAS[item]},
        ],
        "temperature": 0,
    }
    dados = json.dumps(corpo, ensure_ascii=False).encode("utf-8")
    ultimo_erro = ""
    for tentativa in range(1, tentativas + 1):
        inicio = time.perf_counter()
        req = urllib.request.Request(
            ENDPOINT,
            data=dados,
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}",
                "User-Agent": "position-paper-cultural-map/1.0",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=90) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
            conteudo = payload["choices"][0]["message"]["content"]
            pontuacao = converter_resposta(item, conteudo)
            return {
                "variant": variante,
                "item": item,
                "system_prompt": DESCRITORES[variante],
                "user_prompt": PERGUNTAS[item],
                "response_text": conteudo.strip(),
                "score": pontuacao,
                "requested_model": MODEL,
                "response_model": payload.get("model", ""),
                "response_id": payload.get("id", ""),
                "usage": payload.get("usage", {}),
                "temperature": 0,
                "latency_seconds": round(time.perf_counter() - inicio, 4),
                "attempt": tentativa,
                "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                "status": "ok",
            }
        except urllib.error.HTTPError as exc:
            trecho = exc.read(500).decode("utf-8", errors="replace")
            ultimo_erro = f"HTTP {exc.code}: {trecho}"
            if exc.code not in {408, 409, 429, 500, 502, 503, 504}:
                break
        except (urllib.error.URLError, TimeoutError, KeyError, ValueError, json.JSONDecodeError) as exc:
            ultimo_erro = f"{type(exc).__name__}: {exc}"
        if tentativa < tentativas:
            time.sleep(min(2 ** (tentativa - 1), 12))
    return {
        "variant": variante,
        "item": item,
        "system_prompt": DESCRITORES[variante],
        "user_prompt": PERGUNTAS[item],
        "response_text": "",
        "score": None,
        "requested_model": MODEL,
        "response_model": "",
        "response_id": "",
        "usage": {},
        "temperature": 0,
        "latency_seconds": None,
        "attempt": tentativas,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "status": "error",
        "error": ultimo_erro[:500],
    }


def carregar_checkpoint(caminho: Path) -> dict[tuple[int, str], dict[str, Any]]:
    resultados: dict[tuple[int, str], dict[str, Any]] = {}
    if not caminho.exists():
        return resultados
    with caminho.open(encoding="utf-8") as fh:
        for linha in fh:
            if not linha.strip():
                continue
            registro = json.loads(linha)
            if registro.get("status") == "ok":
                resultados[(int(registro["variant"]), registro["item"])] = registro
    return resultados


def escrever_saidas(resultados: list[dict[str, Any]], saida: Path) -> None:
    ordenados = sorted(resultados, key=lambda x: (int(x["variant"]), ITENS.index(x["item"])))

    auditoria = saida / "auditoria-maritaca-sabia4.csv"
    campos = [
        "variant", "item", "score", "response_text", "system_prompt", "user_prompt",
        "requested_model", "response_model", "response_id", "temperature",
        "latency_seconds", "attempt", "timestamp_utc", "status",
        "prompt_tokens", "completion_tokens", "total_tokens",
    ]
    with auditoria.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=campos)
        writer.writeheader()
        for reg in ordenados:
            uso = reg.get("usage") or {}
            linha = {k: reg.get(k, "") for k in campos}
            linha["prompt_tokens"] = uso.get("prompt_tokens", uso.get("input_tokens", ""))
            linha["completion_tokens"] = uso.get("completion_tokens", uso.get("output_tokens", ""))
            linha["total_tokens"] = uso.get("total_tokens", "")
            writer.writerow(linha)

    por_chave = {(int(r["variant"]), r["item"]): r for r in ordenados}
    largo = saida / "respostas-maritaca-sabia4.csv"
    with largo.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=["country", "#variant", *ITENS])
        writer.writeheader()
        for variante in range(10):
            linha: dict[str, Any] = {"country": "general_pt", "#variant": f"variant {variante}"}
            for item in ITENS:
                linha[item] = por_chave[(variante, item)]["score"]
            writer.writerow(linha)

    uso_total = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
    for reg in ordenados:
        uso = reg.get("usage") or {}
        uso_total["prompt_tokens"] += int(uso.get("prompt_tokens", uso.get("input_tokens", 0)) or 0)
        uso_total["completion_tokens"] += int(uso.get("completion_tokens", uso.get("output_tokens", 0)) or 0)
        uso_total["total_tokens"] += int(uso.get("total_tokens", 0) or 0)
    meta = {
        "experiment": "Replicação em português de Tao et al. (2024), expressão cultural padrão",
        "doi": "10.1093/pnasnexus/pgae346",
        "endpoint": ENDPOINT,
        "requested_model": MODEL,
        "response_models": sorted({r.get("response_model", "") for r in ordenados}),
        "language": "pt-BR",
        "cultural_prompt": False,
        "temperature": 0,
        "n_prompt_variants": 10,
        "n_items": 10,
        "n_calls": len(ordenados),
        "first_response_recorded_utc": min(r["timestamp_utc"] for r in ordenados),
        "last_response_recorded_utc": max(r["timestamp_utc"] for r in ordenados),
        "usage": uso_total,
        "translation_note": (
            "Tradução própria das Tabelas 1 e 2; opções, escalas e instruções de formato preservadas."
        ),
        "credential_recorded": False,
    }
    (saida / "metadados-experimento-maritaca-sabia4.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--limit", type=int, default=None, help="Limita chamadas novas para teste.")
    parser.add_argument("--output-dir", type=Path, default=ROOT)
    args = parser.parse_args()

    saida = args.output_dir.resolve()
    saida.mkdir(parents=True, exist_ok=True)
    checkpoint = saida / "respostas-maritaca-sabia4.jsonl"
    prontos = carregar_checkpoint(checkpoint)

    tarefas = [
        (variante, item)
        for variante in range(10)
        for item in ITENS
        if (variante, item) not in prontos
    ]
    if args.limit is not None:
        tarefas = tarefas[: args.limit]

    if tarefas:
        chave = os.environ.get("MARITACA_API_KEY", "")
        if not chave:
            raise SystemExit("Defina MARITACA_API_KEY no ambiente para coletar respostas faltantes.")
        with ThreadPoolExecutor(max_workers=max(1, args.workers)) as pool:
            futuros = {
                pool.submit(chamada, chave, variante, item): (variante, item)
                for variante, item in tarefas
            }
            with checkpoint.open("a", encoding="utf-8") as fh:
                for futuro in as_completed(futuros):
                    registro = futuro.result()
                    fh.write(json.dumps(registro, ensure_ascii=False) + "\n")
                    fh.flush()
                    if registro["status"] == "ok":
                        prontos[(int(registro["variant"]), registro["item"])] = registro
                    else:
                        print(
                            f"Falha na variante {registro['variant']}, item {registro['item']}: "
                            f"{registro.get('error', 'erro desconhecido')}",
                            flush=True,
                        )

    if len(prontos) == 100:
        escrever_saidas(list(prontos.values()), saida)
        print("Experimento concluído: 100/100 respostas válidas.")
    else:
        print(f"Checkpoint atualizado: {len(prontos)}/100 respostas válidas.")


if __name__ == "__main__":
    main()
