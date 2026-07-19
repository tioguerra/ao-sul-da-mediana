#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Strings congeladas das instruções do experimento telefone-sem-fio.

Plano experimental v1.5, seção 6. A instrução é linha única; a única quebra
de linha do prompt separa a instrução do bloco TEXTO. Rode este arquivo para
imprimir os hashes SHA-256 que serão registrados em proveniencia.md no
congelamento (após a revisão do segundo anotador).
"""
import hashlib

PROMPTS = {
    "pt-C1": (
        "Reescreva o texto abaixo. O texto reescrito deve ter aproximadamente "
        "o mesmo número de palavras do texto original. Responda somente com o "
        "texto reescrito, sem comentários.\n\nTEXTO:\n{texto}"
    ),
    "pt-C2": (
        "Reescreva o texto abaixo melhorando a clareza e a qualidade da "
        "escrita. O texto reescrito deve ter aproximadamente o mesmo número "
        "de palavras do texto original. Responda somente com o texto "
        "reescrito, sem comentários.\n\nTEXTO:\n{texto}"
    ),
    "pt-C3": (
        "Reescreva o texto abaixo melhorando a clareza e a qualidade da "
        "escrita, preservando o estilo e o vocabulário regional do texto "
        "original. O texto reescrito deve ter aproximadamente o mesmo número "
        "de palavras do texto original. Responda somente com o texto "
        "reescrito, sem comentários.\n\nTEXTO:\n{texto}"
    ),
    "en-C1": (
        "Rewrite the text below. The rewritten text should have approximately "
        "the same number of words as the original. Respond only with the "
        "rewritten text, without comments.\n\nTEXT:\n{texto}"
    ),
    "en-C2": (
        "Rewrite the text below improving the clarity and the quality of the "
        "writing. The rewritten text should have approximately the same "
        "number of words as the original. Respond only with the rewritten "
        "text, without comments.\n\nTEXT:\n{texto}"
    ),
}

# Quais condições valem para cada grupo de sementes (plano, seção 4).
CONDICOES_POR_GRUPO = {
    "regional": ["pt-C1", "pt-C2", "pt-C3"],
    "controle-pt": ["pt-C1", "pt-C2", "pt-C3"],
    "controle-en": ["en-C1", "en-C2"],
}


def hash_prompt(chave: str) -> str:
    return hashlib.sha256(PROMPTS[chave].encode("utf-8")).hexdigest()


if __name__ == "__main__":
    for chave in PROMPTS:
        print(f"{chave}  sha256:{hash_prompt(chave)}")
