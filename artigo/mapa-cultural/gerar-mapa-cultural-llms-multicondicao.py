#!/usr/bin/env python3
"""Projeta e plota cinco LLMs em quatro condições linguístico-culturais."""

from __future__ import annotations

import importlib.util
import os
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib-cache")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D


ROOT = Path(__file__).resolve().parent
BASE_PATH = ROOT / "gerar-mapa-cultural.py"
SPEC = importlib.util.spec_from_file_location("mapa_base", BASE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("Não foi possível carregar o mapa-base.")
base = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(base)

FUNDO = "#FCFBF8"
MODELOS = {
    "Sabiá-4": {"color": "#0F766E", "marker": "H", "short": "Sabiá-4"},
    "Claude Sonnet 5": {"color": "#C2410C", "marker": "P", "short": "Claude 5"},
    "GPT-5.6 Terra": {"color": "#7C3AED", "marker": "D", "short": "GPT Terra"},
    "Gemini 3.5 Flash": {"color": "#0891B2", "marker": "s", "short": "Gemini Flash"},
    "Grok 4.5": {"color": "#111827", "marker": "X", "short": "Grok 4.5"},
}
CONDICOES = {
    "en_default": "A  |  Perguntas em inglês",
    "pt_default": "B  |  Perguntas em português brasileiro",
    "pt_brazil": "C  |  Português + identidade brasileira",
    "pt_rs": "D  |  Português + identidade gaúcha (RS)",
}


def calcular_coordenadas(beta: np.ndarray) -> tuple[pd.DataFrame, pd.DataFrame]:
    respostas = pd.read_csv(ROOT / "respostas-llms-multicondicao-wide.csv")
    if len(respostas) != 200:
        raise ValueError(f"Esperadas 200 linhas modelo–condição–variante; recebidas {len(respostas)}.")
    linhas = []
    for _, linha in respostas.iterrows():
        xy = base.pontuar(linha[base.ITENS].to_numpy(float), beta)
        registro = {
            "backend": linha["backend"],
            "model_label": linha["model_label"],
            "requested_model": linha["requested_model"],
            "condition": linha["condition"],
            "condition_label": linha["condition_label"],
            "prompt_language": linha["prompt_language"],
            "cultural_identity": linha["cultural_identity"],
            "variant": int(linha["variant"]),
            "x_survival_self_expression": float(xy[0]),
            "y_traditional_secular": float(xy[1]),
        }
        registro.update(
            {
                item: int(linha[item]) if pd.notna(linha[item]) else np.nan
                for item in base.ITENS
            }
        )
        linhas.append(registro)
    variantes = pd.DataFrame(linhas)
    chaves = [
        "backend", "model_label", "requested_model", "condition",
        "condition_label", "prompt_language", "cultural_identity",
    ]
    medias_linhas = []
    for valores, grupo in variantes.groupby(chaves, sort=False, dropna=False):
        medias_itens = grupo[base.ITENS].mean(skipna=True)
        xy = base.pontuar(medias_itens.to_numpy(float), beta)
        completas = grupo.dropna(subset=base.ITENS)
        registro = dict(zip(chaves, valores))
        registro.update(
            {
                "x_survival_self_expression": float(xy[0]),
                "y_traditional_secular": float(xy[1]),
                "n_prompt_variants": int(len(grupo)),
                "n_complete_variants": int(len(completas)),
                "n_scored_responses": int(grupo[base.ITENS].count().sum()),
                "n_invalid_responses": int(grupo[base.ITENS].isna().sum().sum()),
                "min_responses_per_item": int(grupo[base.ITENS].count().min()),
                "sd_x_between_complete_variants": float(completas["x_survival_self_expression"].std()),
                "sd_y_between_complete_variants": float(completas["y_traditional_secular"].std()),
                "min_x_complete_variants": float(completas["x_survival_self_expression"].min()),
                "max_x_complete_variants": float(completas["x_survival_self_expression"].max()),
                "min_y_complete_variants": float(completas["y_traditional_secular"].min()),
                "max_y_complete_variants": float(completas["y_traditional_secular"].max()),
            }
        )
        registro.update({f"mean_{item}": float(medias_itens[item]) for item in base.ITENS})
        medias_linhas.append(registro)
    medias = pd.DataFrame(medias_linhas)
    return variantes, medias


def calcular_distancias(medias: pd.DataFrame, humanos: pd.DataFrame) -> pd.DataFrame:
    referencias = {
        "Argentina": "Argentina",
        "Brazil": "Brasil",
        "Uruguay": "Uruguai",
        "Rio Grande do Sul": "Rio Grande do Sul",
    }
    linhas = []
    for _, modelo in medias.iterrows():
        for chave, rotulo in referencias.items():
            humano = humanos[humanos["entity"] == chave].iloc[0]
            distancia = float(
                np.hypot(
                    modelo["x_survival_self_expression"] - humano["x_survival_self_expression"],
                    modelo["y_traditional_secular"] - humano["y_traditional_secular"],
                )
            )
            linhas.append(
                {
                    "model_label": modelo["model_label"],
                    "requested_model": modelo["requested_model"],
                    "condition": modelo["condition"],
                    "condition_label": modelo["condition_label"],
                    "reference": rotulo,
                    "distance": distancia,
                }
            )
    return pd.DataFrame(linhas)


def gerar_figura(
    variantes: pd.DataFrame,
    medias: pd.DataFrame,
    dados_base: pd.DataFrame,
) -> None:
    paises = dados_base[dados_base["entity_type"] == "country_human"]
    humanos = dados_base[
        dados_base["entity"].isin(["Argentina", "Brazil", "Uruguay", "Rio Grande do Sul"])
    ]
    rs = dict(base.RS_PRECALCULADO)

    todos_x = pd.concat(
        [paises["x_survival_self_expression"], variantes["x_survival_self_expression"]]
    )
    todos_y = pd.concat(
        [paises["y_traditional_secular"], variantes["y_traditional_secular"]]
    )
    xlim = (min(-1.75, float(todos_x.min()) - 0.25), max(3.90, float(todos_x.max()) + 0.25))
    ylim = (min(-2.10, float(todos_y.min()) - 0.25), max(2.00, float(todos_y.max()) + 0.25))

    plt.rcParams.update({"font.family": "DejaVu Sans", "axes.titleweight": "bold"})
    fig, axs = plt.subplots(
        2, 2, figsize=(16.4, 11.3), sharex=True, sharey=True,
        facecolor=FUNDO, gridspec_kw={"hspace": 0.20, "wspace": 0.10},
    )
    axs = axs.ravel()

    offsets_humanos = {
        "Argentina": (5, 5), "Brazil": (-37, -13),
        "Uruguay": (5, -13), "Rio Grande do Sul": (5, 6),
    }
    for ax, (condicao, titulo) in zip(axs, CONDICOES.items()):
        base.estilo_eixos(ax)
        ax.scatter(
            paises["x_survival_self_expression"], paises["y_traditional_secular"],
            s=17, color="#A8B0BB", alpha=0.56, edgecolor="white", linewidth=0.25, zorder=1,
        )
        base.adicionar_elipse(ax, rs)
        for _, linha in humanos.iterrows():
            nome = linha["entity"]
            marcador = "*" if nome == "Rio Grande do Sul" else "o"
            ax.scatter(
                linha["x_survival_self_expression"], linha["y_traditional_secular"],
                s=145 if marcador == "*" else 70, marker=marcador,
                color=base.CORES[nome], edgecolor="white", linewidth=0.9, zorder=6,
            )
            ax.annotate(
                base.ROTULOS[nome],
                (linha["x_survival_self_expression"], linha["y_traditional_secular"]),
                xytext=offsets_humanos[nome], textcoords="offset points",
                fontsize=6.9, weight="bold", color=base.CORES[nome],
                bbox=dict(facecolor=FUNDO, edgecolor="none", alpha=0.84, pad=0.7), zorder=7,
            )

        if condicao == "pt_brazil":
            alvo = humanos[humanos["entity"] == "Brazil"].iloc[0]
            ax.scatter(
                [alvo["x_survival_self_expression"]], [alvo["y_traditional_secular"]],
                s=180, facecolor="none", edgecolor=base.CORES["Brazil"],
                linewidth=1.5, linestyle="--", zorder=5,
            )
        elif condicao == "pt_rs":
            alvo = humanos[humanos["entity"] == "Rio Grande do Sul"].iloc[0]
            ax.scatter(
                [alvo["x_survival_self_expression"]], [alvo["y_traditional_secular"]],
                s=255, facecolor="none", edgecolor=base.CORES["Rio Grande do Sul"],
                linewidth=1.5, linestyle="--", zorder=5,
            )

        for modelo, estilo in MODELOS.items():
            vars_modelo = variantes[
                (variantes["condition"] == condicao)
                & (variantes["model_label"] == modelo)
            ]
            media = medias[
                (medias["condition"] == condicao)
                & (medias["model_label"] == modelo)
            ]
            if vars_modelo.empty or media.empty:
                continue
            ax.scatter(
                vars_modelo["x_survival_self_expression"],
                vars_modelo["y_traditional_secular"],
                s=20, marker="o", facecolor=estilo["color"], edgecolor="none",
                alpha=0.23, zorder=3,
            )
            ax.scatter(
                media["x_survival_self_expression"],
                media["y_traditional_secular"],
                s=115, marker=estilo["marker"], facecolor=estilo["color"],
                edgecolor="white", linewidth=1.0, zorder=8,
            )

        ax.set_xlim(*xlim)
        ax.set_ylim(*ylim)
        ax.set_title(titulo, loc="left", fontsize=11.0, color="#273142", pad=8)

    # Rótulos dos eixos apenas nas bordas, reduzindo repetição visual.
    for ax in axs[:2]:
        ax.set_xlabel("")
    for ax in [axs[1], axs[3]]:
        ax.set_ylabel("")

    legenda_modelos = [
        Line2D(
            [0], [0], marker=estilo["marker"], color="none",
            markerfacecolor=estilo["color"], markeredgecolor="white",
            markersize=8.5, label=estilo["short"],
        )
        for estilo in MODELOS.values()
    ]
    legenda_humanos = [
        Line2D([0], [0], marker="o", color="none", markerfacecolor="#8E98A5", markeredgecolor="white", markersize=7, label="107 países — IVS"),
        Line2D([0], [0], marker="o", color="none", markerfacecolor=base.CORES["Brazil"], markeredgecolor="white", markersize=7, label="Brasil"),
        Line2D([0], [0], marker="o", color="none", markerfacecolor=base.CORES["Argentina"], markeredgecolor="white", markersize=7, label="Argentina"),
        Line2D([0], [0], marker="o", color="none", markerfacecolor=base.CORES["Uruguay"], markeredgecolor="white", markersize=7, label="Uruguai"),
        Line2D([0], [0], marker="*", color="none", markerfacecolor=base.CORES["Rio Grande do Sul"], markeredgecolor="white", markersize=11, label="RS — estimativa exploratória"),
        Line2D([0], [0], marker="o", color="none", markerfacecolor="#667085", markeredgecolor="none", alpha=0.28, markersize=6, label="Perfis completos"),
    ]
    fig.legend(
        handles=legenda_modelos + legenda_humanos,
        loc="upper center", bbox_to_anchor=(0.5, 0.900), ncol=11,
        frameon=False, fontsize=8.1, columnspacing=1.0, handletextpad=0.4,
    )
    fig.suptitle(
        "Mapa cultural multilíngue: cinco LLMs em quatro condições",
        x=0.055, y=0.985, ha="left", fontsize=19, weight="bold", color="#182230",
    )
    fig.text(
        0.056, 0.948,
        "Símbolo grande: projeção das médias por pergunta em 10 formulações; pontos translúcidos: perfis completos de cada formulação.",
        ha="left", va="top", fontsize=9.7, color="#4B5563",
    )
    n_pontuadas = f"{int(medias['n_scored_responses'].sum()):,}".replace(",", ".")
    fig.text(
        0.056, 0.018,
        (
            "Fontes humanas: Tao et al. (2024), OSF 7sj3w; RS: WVS 7 v6.0, Brasil 2018, n=118 completos. "
            f"LLMs: experimento próprio via OpenRouter e Maritaca API, jul. 2026; {n_pontuadas}/2.000 respostas pontuadas. Temperatura 0 solicitada; "
            "OpenRouter não anunciava suporte nativo a esse parâmetro para Claude Sonnet 5 e GPT-5.6 Terra."
        ),
        ha="left", va="bottom", fontsize=7.5, color="#5F6875",
    )
    fig.subplots_adjust(top=0.835, bottom=0.095, left=0.075, right=0.985)

    for ext, kwargs in [("png", {"dpi": 240}), ("svg", {}), ("pdf", {})]:
        fig.savefig(
            ROOT / f"figura-mapa-cultural-llms-multicondicao.{ext}",
            bbox_inches="tight", facecolor=fig.get_facecolor(), **kwargs,
        )
    plt.close(fig)


def main() -> None:
    beta, residuo = base.inferir_transformacao()
    if residuo > 1e-10:
        raise RuntimeError(f"Transformação não recuperada com precisão: {residuo:g}")
    dados_base = base.montar_dados(beta, dict(base.RS_PRECALCULADO))
    variantes, medias = calcular_coordenadas(beta)
    humanos = dados_base[
        dados_base["entity"].isin(["Argentina", "Brazil", "Uruguay", "Rio Grande do Sul"])
    ]
    distancias = calcular_distancias(medias, humanos)
    variantes.to_csv(ROOT / "coordenadas-llms-multicondicao-variantes.csv", index=False)
    medias.to_csv(ROOT / "coordenadas-llms-multicondicao-medias.csv", index=False)
    distancias.to_csv(ROOT / "distancias-llms-multicondicao.csv", index=False)
    gerar_figura(variantes, medias, dados_base)
    print(medias[["model_label", "condition", "x_survival_self_expression", "y_traditional_secular"]].to_string(index=False))


if __name__ == "__main__":
    main()
