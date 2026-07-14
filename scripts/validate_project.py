#!/usr/bin/env python3
"""Validação offline da estrutura, dos dados e de padrões comuns de segredos."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "README.md",
    "LICENSE",
    "LICENSE-CONTENT.md",
    "THIRD_PARTY_NOTICES.md",
    "DATA_AVAILABILITY.md",
    "CITATION.cff",
    "requirements.txt",
    "CHECKSUMS.sha256",
    "artigo/banco-de-evidencias.md",
    "artigo/referencias-chave.bib",
    "artigo/mapa-cultural/analise-resultados-distancias-llms.md",
    "artigo/mapa-cultural/figura-mapa-cultural-quatro-condicoes-trajetorias.png",
    "manuscrito/original/resumo-expandido.docx",
]

EXPECTED_CSV_ROWS = {
    "artigo/mapa-cultural/auditoria-llms-multicondicao.csv": 2000,
    "artigo/mapa-cultural/respostas-llms-multicondicao-wide.csv": 200,
    "artigo/mapa-cultural/coordenadas-llms-multicondicao-variantes.csv": 200,
    "artigo/mapa-cultural/coordenadas-llms-multicondicao-medias.csv": 20,
    "artigo/mapa-cultural/distancias-modelos-paises-interesse-e-vizinhos.csv": 20,
    "artigo/mapa-cultural/deslocamentos-modelos-entre-condicoes.csv": 30,
    "artigo/mapa-cultural/efeitos-prompts-culturais-alvos.csv": 10,
    "artigo/mapa-cultural/efeitos-prompts-todas-referencias.csv": 40,
    "artigo/mapa-cultural/contribuicoes-itens-deslocamentos-culturais.csv": 100,
}

EXPECTED_JSONL_ROWS = {
    "artigo/mapa-cultural/respostas-openrouter-multicondicao.jsonl": 1601,
    "artigo/mapa-cultural/respostas-maritaca-condicoes-adicionais.jsonl": 300,
    "artigo/mapa-cultural/respostas-maritaca-sabia4.jsonl": 100,
}

TEXT_SUFFIXES = {
    ".bib", ".cff", ".csv", ".json", ".jsonl", ".md", ".py", ".R",
    ".txt", ".yaml", ".yml", "",
}

SECRET_PATTERNS = {
    "OpenRouter": re.compile(r"\bsk-or-v1-[A-Za-z0-9_-]{20,}\b"),
    "chave estilo Maritaca": re.compile(r"\b\d{12,}_[a-fA-F0-9]{20,}\b"),
    "atribuição de chave": re.compile(
        r"(?i)(?:OPENROUTER_API_KEY|MARITACA_API_KEY)\s*=\s*['\"]?[^\s'\"]{12,}"
    ),
    "Bearer literal": re.compile(r"(?i)Authorization.{0,40}Bearer\s+[A-Za-z0-9._-]{20,}"),
}


def fail(message: str, errors: list[str]) -> None:
    errors.append(message)


def validate_required(errors: list[str]) -> None:
    for relative in REQUIRED_FILES:
        path = ROOT / relative
        if not path.is_file() or path.stat().st_size == 0:
            fail(f"arquivo obrigatório ausente ou vazio: {relative}", errors)


def validate_csv(errors: list[str]) -> None:
    for relative, expected in EXPECTED_CSV_ROWS.items():
        path = ROOT / relative
        try:
            with path.open(encoding="utf-8", newline="") as handle:
                reader = csv.reader(handle)
                header = next(reader)
                rows = sum(1 for _ in reader)
            if not header:
                fail(f"CSV sem cabeçalho: {relative}", errors)
            if rows != expected:
                fail(f"{relative}: {rows} linhas; esperado {expected}", errors)
        except Exception as exc:  # noqa: BLE001
            fail(f"falha ao ler {relative}: {exc}", errors)


def validate_jsonl(errors: list[str]) -> None:
    for relative, expected in EXPECTED_JSONL_ROWS.items():
        path = ROOT / relative
        count = 0
        try:
            with path.open(encoding="utf-8") as handle:
                for line_number, line in enumerate(handle, start=1):
                    if not line.strip():
                        continue
                    json.loads(line)
                    count += 1
            if count != expected:
                fail(f"{relative}: {count} registros; esperado {expected}", errors)
        except Exception as exc:  # noqa: BLE001
            fail(f"JSONL inválido em {relative}, linha {line_number}: {exc}", errors)


def validate_secrets(errors: list[str]) -> None:
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts or ".venv" in path.parts:
            continue
        if path.suffix not in TEXT_SUFFIXES and path.name not in {"Makefile", "LICENSE"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        relative = path.relative_to(ROOT)
        for label, pattern in SECRET_PATTERNS.items():
            match = pattern.search(text)
            if match:
                value = match.group(0)
                if value.endswith("_API_KEY=") or value.endswith("_API_KEY=\""):
                    continue
                fail(f"possível segredo ({label}) em {relative}", errors)


def validate_restricted_data(errors: list[str]) -> None:
    forbidden_suffixes = {".sav", ".zsav", ".dta"}
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        lower = path.name.lower()
        if path.suffix.lower() in forbidden_suffixes:
            fail(f"possível microdado restrito: {path.relative_to(ROOT)}", errors)
        if "wvs_cross-national" in lower:
            fail(f"arquivo WVS não redistribuível: {path.relative_to(ROOT)}", errors)


def validate_checksums(errors: list[str]) -> None:
    manifest = ROOT / "CHECKSUMS.sha256"
    line_number = 0
    try:
        for line_number, line in enumerate(manifest.read_text(encoding="utf-8").splitlines(), start=1):
            if not line.strip():
                continue
            expected, relative = line.split(maxsplit=1)
            path = ROOT / relative
            if not path.is_file():
                fail(f"checksum aponta para arquivo ausente: {relative}", errors)
                continue
            observed = hashlib.sha256(path.read_bytes()).hexdigest()
            if observed != expected:
                fail(f"checksum divergente: {relative}", errors)
    except Exception as exc:  # noqa: BLE001
        fail(f"manifesto de checksums inválido na linha {line_number}: {exc}", errors)


def main() -> int:
    errors: list[str] = []
    validate_required(errors)
    validate_csv(errors)
    validate_jsonl(errors)
    validate_secrets(errors)
    validate_restricted_data(errors)
    validate_checksums(errors)
    if errors:
        print("Validação falhou:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("Validação concluída: estrutura, contagens, JSONL, segredos e microdados.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
