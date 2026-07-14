#!/usr/bin/env python3
"""Calcula distâncias dos cinco LLMs a referências humanas e entre condições."""

from __future__ import annotations

import importlib.util
import itertools
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parent
BASE_PATH = ROOT / "gerar-mapa-cultural.py"
SPEC = importlib.util.spec_from_file_location("mapa_base", BASE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("Não foi possível carregar o mapa-base.")
base = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(base)

MODELOS = ["Sabiá-4", "Claude Sonnet 5", "GPT-5.6 Terra", "Gemini 3.5 Flash", "Grok 4.5"]
CONDICOES = ["en_default", "pt_default", "pt_brazil", "pt_rs"]
ROTULOS_CONDICAO = {
    "en_default": "1 — Inglês",
    "pt_default": "2 — Português",
    "pt_brazil": "3 — Identidade brasileira",
    "pt_rs": "4 — Identidade gaúcha",
}
REFERENCIAS = {
    "Brazil": "Brasil",
    "Argentina": "Argentina",
    "Uruguay": "Uruguai",
    "Rio Grande do Sul": "Rio Grande do Sul",
}
ROTULOS_ITENS = {
    "a008": "Felicidade",
    "a165": "Confiança interpessoal",
    "e018": "Respeito pela autoridade",
    "e025": "Assinatura de petição",
    "f063": "Importância de Deus",
    "f118": "Justificabilidade da homossexualidade",
    "f120": "Justificabilidade do aborto",
    "g006": "Orgulho nacional",
    "y002": "Prioridades materialistas/pós-materialistas",
    "y003": "Qualidades valorizadas nas crianças",
}
TRADUCOES = {
    "Brazil": "Brasil",
    "Argentina": "Argentina",
    "Uruguay": "Uruguai",
    "North Ireland": "Irlanda do Norte",
    "United States": "Estados Unidos",
    "Japan": "Japão",
    "Germany": "Alemanha",
    "Mongolia": "Mongólia",
    "Slovenia": "Eslovênia",
    "Vietnam": "Vietnã",
    "Czechia": "Tchéquia",
    "Mexico": "México",
    "Ireland": "Irlanda",
    "Spain": "Espanha",
    "Estonia": "Estônia",
    "Finland": "Finlândia",
    "Andorra": "Andorra",
    "Austria": "Áustria",
    "Belgium": "Bélgica",
    "Puerto Rico": "Porto Rico",
    "Italy": "Itália",
    "Haiti": "Haiti",
    "Malta": "Malta",
    "South Africa": "África do Sul",
}


def distancia(a: pd.Series, b: pd.Series) -> float:
    return float(
        np.hypot(
            a["x_survival_self_expression"] - b["x_survival_self_expression"],
            a["y_traditional_secular"] - b["y_traditional_secular"],
        )
    )


def carregar() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    beta, residuo = base.inferir_transformacao()
    if residuo > 1e-10:
        raise RuntimeError(f"Transformação imprecisa: {residuo:g}")
    dados = base.montar_dados(beta, dict(base.RS_PRECALCULADO))
    paises = dados[dados["entity_type"] == "country_human"].copy()
    referencias = dados[dados["entity"].isin(REFERENCIAS)].copy().set_index("entity")
    modelos = pd.read_csv(ROOT / "coordenadas-llms-multicondicao-medias.csv")
    modelos["model_label"] = pd.Categorical(modelos["model_label"], MODELOS, ordered=True)
    modelos["condition"] = pd.Categorical(modelos["condition"], CONDICOES, ordered=True)
    modelos = modelos.sort_values(["model_label", "condition"]).reset_index(drop=True)
    if len(paises) != 107 or len(referencias) != 4 or len(modelos) != 20:
        raise ValueError("Dimensões inesperadas nas bases de entrada.")
    return paises, referencias, modelos


def tabela_distancias(
    paises: pd.DataFrame,
    referencias: pd.DataFrame,
    modelos: pd.DataFrame,
) -> pd.DataFrame:
    linhas = []
    for _, ponto in modelos.iterrows():
        candidatos = paises.copy()
        candidatos["distance"] = np.hypot(
            candidatos["x_survival_self_expression"] - ponto["x_survival_self_expression"],
            candidatos["y_traditional_secular"] - ponto["y_traditional_secular"],
        )
        proximos = candidatos.nsmallest(3, "distance").reset_index(drop=True)
        dist_interesse = {
            f"distance_{rotulo.lower().replace(' ', '_')}": distancia(ponto, referencias.loc[chave])
            for chave, rotulo in REFERENCIAS.items()
        }
        rotulos_interesse = {
            f"distance_{rotulo.lower().replace(' ', '_')}": rotulo
            for rotulo in REFERENCIAS.values()
        }
        interesse_mais_proximo = min(dist_interesse, key=dist_interesse.get)
        registro = {
            "model_label": str(ponto["model_label"]),
            "requested_model": ponto["requested_model"],
            "condition": str(ponto["condition"]),
            "condition_label": ROTULOS_CONDICAO[str(ponto["condition"])],
            "x_survival_self_expression": ponto["x_survival_self_expression"],
            "y_traditional_secular": ponto["y_traditional_secular"],
            **dist_interesse,
            "nearest_interest_reference": rotulos_interesse[interesse_mais_proximo],
            "nearest_interest_distance": dist_interesse[interesse_mais_proximo],
        }
        for ordem, vizinho in proximos.iterrows():
            n = int(ordem) + 1
            registro[f"nearest_country_{n}"] = TRADUCOES.get(vizinho["entity"], vizinho["entity"])
            registro[f"nearest_country_{n}_source_name"] = vizinho["entity"]
            registro[f"nearest_country_{n}_distance"] = vizinho["distance"]
        linhas.append(registro)
    return pd.DataFrame(linhas)


def tabela_deslocamentos(modelos: pd.DataFrame) -> pd.DataFrame:
    linhas = []
    for modelo in MODELOS:
        grupo = modelos[modelos["model_label"] == modelo].set_index("condition")
        for condicao_a, condicao_b in itertools.combinations(CONDICOES, 2):
            a = grupo.loc[condicao_a]
            b = grupo.loc[condicao_b]
            dx = float(b["x_survival_self_expression"] - a["x_survival_self_expression"])
            dy = float(b["y_traditional_secular"] - a["y_traditional_secular"])
            linhas.append(
                {
                    "model_label": modelo,
                    "condition_a": condicao_a,
                    "condition_a_label": ROTULOS_CONDICAO[condicao_a],
                    "condition_b": condicao_b,
                    "condition_b_label": ROTULOS_CONDICAO[condicao_b],
                    "delta_x": dx,
                    "delta_y": dy,
                    "distance_between_conditions": float(np.hypot(dx, dy)),
                }
            )
    return pd.DataFrame(linhas)


def tabela_mudancas(
    referencias: pd.DataFrame,
    modelos: pd.DataFrame,
) -> pd.DataFrame:
    linhas = []
    intervencoes = [
        ("pt_brazil", "Identidade brasileira", "Brazil", "Brasil"),
        ("pt_rs", "Identidade gaúcha", "Rio Grande do Sul", "Rio Grande do Sul"),
    ]
    for modelo in MODELOS:
        grupo = modelos[modelos["model_label"] == modelo].set_index("condition")
        base_pt = grupo.loc["pt_default"]
        for condicao, intervencao, alvo_chave, alvo_rotulo in intervencoes:
            ponto = grupo.loc[condicao]
            d0 = distancia(base_pt, referencias.loc[alvo_chave])
            d1 = distancia(ponto, referencias.loc[alvo_chave])
            linhas.append(
                {
                    "model_label": modelo,
                    "intervention_condition": condicao,
                    "intervention": intervencao,
                    "target": alvo_rotulo,
                    "baseline_distance_pt_default": d0,
                    "prompted_distance": d1,
                    "absolute_change_prompt_minus_baseline": d1 - d0,
                    "relative_change_percent": 100 * (d1 - d0) / d0,
                    "improved_alignment": d1 < d0,
                }
            )
    return pd.DataFrame(linhas)


def tabela_mudancas_todas_referencias(
    referencias: pd.DataFrame,
    modelos: pd.DataFrame,
) -> pd.DataFrame:
    linhas = []
    for modelo in MODELOS:
        grupo = modelos[modelos["model_label"] == modelo].set_index("condition")
        base_pt = grupo.loc["pt_default"]
        for condicao in ["pt_brazil", "pt_rs"]:
            ponto = grupo.loc[condicao]
            for chave, rotulo in REFERENCIAS.items():
                d0 = distancia(base_pt, referencias.loc[chave])
                d1 = distancia(ponto, referencias.loc[chave])
                linhas.append(
                    {
                        "model_label": modelo,
                        "intervention_condition": condicao,
                        "intervention_label": ROTULOS_CONDICAO[condicao],
                        "reference": rotulo,
                        "baseline_distance_pt_default": d0,
                        "prompted_distance": d1,
                        "absolute_change_prompt_minus_baseline": d1 - d0,
                        "relative_change_percent": 100 * (d1 - d0) / d0,
                    }
                )
    return pd.DataFrame(linhas)


def tabela_contribuicoes_itens(modelos: pd.DataFrame) -> pd.DataFrame:
    """Decompõe cada deslocamento cultural na transformação linear dos dez itens."""

    beta, residuo = base.inferir_transformacao()
    if residuo > 1e-10:
        raise RuntimeError(f"Transformação imprecisa: {residuo:g}")
    linhas = []
    for modelo in MODELOS:
        grupo = modelos[modelos["model_label"] == modelo].set_index("condition")
        for condicao in ["pt_brazil", "pt_rs"]:
            for indice, item in enumerate(base.ITENS, start=1):
                media_base = float(grupo.loc["pt_default", f"mean_{item}"])
                media_prompt = float(grupo.loc[condicao, f"mean_{item}"])
                delta_item = media_prompt - media_base
                contribuicao_x = delta_item * float(beta[indice, 0])
                contribuicao_y = delta_item * float(beta[indice, 1])
                linhas.append(
                    {
                        "model_label": modelo,
                        "intervention_condition": condicao,
                        "intervention_label": ROTULOS_CONDICAO[condicao],
                        "item": item,
                        "item_label": ROTULOS_ITENS[item],
                        "baseline_item_mean_pt_default": media_base,
                        "prompted_item_mean": media_prompt,
                        "item_mean_change": delta_item,
                        "coefficient_x": float(beta[indice, 0]),
                        "coefficient_y": float(beta[indice, 1]),
                        "contribution_to_delta_x": contribuicao_x,
                        "contribution_to_delta_y": contribuicao_y,
                        "contribution_vector_magnitude": float(
                            np.hypot(contribuicao_x, contribuicao_y)
                        ),
                    }
                )
    return pd.DataFrame(linhas)


def main() -> None:
    paises, referencias, modelos = carregar()
    distancias = tabela_distancias(paises, referencias, modelos)
    deslocamentos = tabela_deslocamentos(modelos)
    mudancas = tabela_mudancas(referencias, modelos)
    mudancas_todas = tabela_mudancas_todas_referencias(referencias, modelos)
    contribuicoes = tabela_contribuicoes_itens(modelos)
    distancias.to_csv(ROOT / "distancias-modelos-paises-interesse-e-vizinhos.csv", index=False)
    deslocamentos.to_csv(ROOT / "deslocamentos-modelos-entre-condicoes.csv", index=False)
    mudancas.to_csv(ROOT / "efeitos-prompts-culturais-alvos.csv", index=False)
    mudancas_todas.to_csv(ROOT / "efeitos-prompts-todas-referencias.csv", index=False)
    contribuicoes.to_csv(
        ROOT / "contribuicoes-itens-deslocamentos-culturais.csv", index=False
    )
    print(distancias[[
        "model_label", "condition", "distance_brasil", "distance_argentina",
        "distance_uruguai", "distance_rio_grande_do_sul", "nearest_country_1",
        "nearest_country_1_distance",
    ]].to_string(index=False))


if __name__ == "__main__":
    main()
