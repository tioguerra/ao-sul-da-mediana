#!/usr/bin/env python3
"""Acrescenta o experimento Sabiá-4 em português ao mapa cultural."""

from __future__ import annotations

import importlib.util
import math
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
    raise RuntimeError("Não foi possível carregar o gerador do mapa-base.")
base = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(base)

MARITACA = "#0F766E"
GPT = "#7C3AED"
FUNDO = "#FCFBF8"


def calcular_maritaca(beta: np.ndarray) -> tuple[pd.DataFrame, pd.Series]:
    respostas = pd.read_csv(ROOT / "respostas-maritaca-sabia4.csv")
    faltantes = [c for c in base.ITENS if c not in respostas]
    if faltantes or len(respostas) != 10:
        raise ValueError(f"Matriz Sabiá incompleta: {faltantes=}, linhas={len(respostas)}")

    linhas = []
    for indice, linha in respostas.iterrows():
        xy = base.pontuar(linha[base.ITENS].to_numpy(float), beta)
        registro = {
            "variant": int(str(linha["#variant"]).split()[-1]),
            "x_survival_self_expression": float(xy[0]),
            "y_traditional_secular": float(xy[1]),
        }
        registro.update({item: int(linha[item]) for item in base.ITENS})
        linhas.append(registro)
    variantes = pd.DataFrame(linhas).sort_values("variant")
    media = variantes[["x_survival_self_expression", "y_traditional_secular"]].mean()
    return variantes, media


def montar_dados(beta: np.ndarray, variantes: pd.DataFrame, media: pd.Series) -> pd.DataFrame:
    dados = base.montar_dados(beta, dict(base.RS_PRECALCULADO))
    dados = dados[dados["entity_type"] != "ai_cultural_prompt"].copy()
    novas = []
    for _, linha in variantes.iterrows():
        novas.append(
            {
                "entity": f"Sabiá-4 — variante {int(linha['variant'])}",
                "entity_type": "ai_default_prompt_variant_pt",
                "model_version": "sabia-4",
                "reference_entity": "",
                "x_survival_self_expression": linha["x_survival_self_expression"],
                "y_traditional_secular": linha["y_traditional_secular"],
                "source": "Experimento próprio via Maritaca API",
                "notes": "Português; sem identidade cultural; temperatura 0.",
            }
        )
    novas.append(
        {
            "entity": "Sabiá-4",
            "entity_type": "ai_default_pt",
            "model_version": "sabia-4",
            "reference_entity": "",
            "x_survival_self_expression": media["x_survival_self_expression"],
            "y_traditional_secular": media["y_traditional_secular"],
            "source": "Experimento próprio via Maritaca API",
            "notes": "Média de dez descritores genéricos em português; sem identidade cultural; temperatura 0.",
        }
    )
    return pd.concat([dados, pd.DataFrame(novas)], ignore_index=True)


def gerar_figura(dados: pd.DataFrame, variantes: pd.DataFrame, media: pd.Series) -> None:
    paises = dados[dados["entity_type"] == "country_human"]
    gpts = dados[dados["entity_type"] == "ai_default"]
    regionais = dados[
        dados["entity"].isin(["Argentina", "Brazil", "Uruguay", "Rio Grande do Sul"])
    ]

    plt.rcParams.update({"font.family": "DejaVu Sans", "axes.titleweight": "bold"})
    fig, ax = plt.subplots(figsize=(13.6, 8.6), facecolor=FUNDO)
    base.estilo_eixos(ax)

    ax.scatter(
        paises["x_survival_self_expression"],
        paises["y_traditional_secular"],
        s=31,
        color="#A8B0BB",
        alpha=0.70,
        edgecolor="white",
        linewidth=0.4,
        zorder=1,
    )

    contexto = {
        "Canada": (5, 5), "Sweden": (5, 5),
        "Germany": (5, 5), "Japan": (5, 5), "China": (5, 5),
        "Russia": (5, 5), "India": (5, -11), "Nigeria": (5, -11),
        "South Africa": (5, 5), "Australia": (5, -11), "Spain": (5, 5),
    }
    for nome, deslocamento in contexto.items():
        linha = paises[paises["entity"] == nome]
        if linha.empty:
            continue
        x, y = linha.iloc[0][["x_survival_self_expression", "y_traditional_secular"]]
        ax.annotate(
            nome, (x, y), xytext=deslocamento, textcoords="offset points",
            fontsize=7.0, color="#7B8491", alpha=0.95, zorder=2,
        )

    base.adicionar_elipse(ax, dict(base.RS_PRECALCULADO))
    offsets_regiao = {
        "Argentina": (7, 8),
        "Brazil": (-48, -16),
        "Uruguay": (8, -16),
        "Rio Grande do Sul": (8, 9),
    }
    for _, linha in regionais.iterrows():
        nome = linha["entity"]
        marcador = "*" if nome == "Rio Grande do Sul" else "o"
        ax.scatter(
            linha["x_survival_self_expression"], linha["y_traditional_secular"],
            s=250 if marcador == "*" else 125, marker=marcador,
            color=base.CORES[nome], edgecolor="white", linewidth=1.2, zorder=7,
        )
        ax.annotate(
            base.ROTULOS[nome] + (" (2018)" if nome == "Rio Grande do Sul" else ""),
            (linha["x_survival_self_expression"], linha["y_traditional_secular"]),
            xytext=offsets_regiao[nome], textcoords="offset points", fontsize=9.0,
            weight="bold", color=base.CORES[nome],
            bbox=dict(facecolor=FUNDO, edgecolor="none", alpha=0.9, pad=1.4), zorder=8,
        )

    ax.scatter(
        gpts["x_survival_self_expression"], gpts["y_traditional_secular"],
        s=115, marker="D", facecolor=GPT, edgecolor="white", linewidth=1.1, zorder=7,
    )
    offsets_gpt = {
        "GPT-3": (9, -5), "GPT-3.5": (7, 10), "GPT-4": (9, 8),
        "GPT-4 Turbo": (9, -12), "GPT-4o": (-44, 10),
    }
    for _, linha in gpts.iterrows():
        ax.annotate(
            linha["entity"],
            (linha["x_survival_self_expression"], linha["y_traditional_secular"]),
            xytext=offsets_gpt[linha["entity"]], textcoords="offset points",
            fontsize=8.5, weight="bold", color="#6D28D9",
            bbox=dict(facecolor=FUNDO, edgecolor="none", alpha=0.9, pad=1.2), zorder=8,
        )

    # Formulações individuais: dispersão devida somente ao descritor, pois T=0.
    ax.scatter(
        variantes["x_survival_self_expression"], variantes["y_traditional_secular"],
        s=52, marker="o", facecolor=FUNDO, edgecolor=MARITACA,
        linewidth=1.35, alpha=0.82, zorder=5,
    )
    mx = float(media["x_survival_self_expression"])
    my = float(media["y_traditional_secular"])
    ax.scatter(
        [mx], [my], s=245, marker="H", facecolor=MARITACA,
        edgecolor="white", linewidth=1.4, zorder=9,
    )
    ax.annotate(
        "Sabiá-4\n(português)", (mx, my), xytext=(11, -36), textcoords="offset points",
        fontsize=10.0, weight="bold", color=MARITACA,
        bbox=dict(facecolor=FUNDO, edgecolor="none", alpha=0.93, pad=1.8), zorder=10,
    )

    # O país mais próximo do ponto médio do Sabiá-4 é destacado sem alterar
    # o símbolo que representa a observação humana.
    eua = paises[paises["entity"] == "United States"].iloc[0]
    ux = float(eua["x_survival_self_expression"])
    uy = float(eua["y_traditional_secular"])
    distancia_eua = math.hypot(mx - ux, my - uy)
    ax.plot([mx, ux], [my, uy], color=MARITACA, linewidth=1.1, linestyle=(0, (3, 3)), alpha=0.72, zorder=4)
    ax.scatter([ux], [uy], s=44, color="#667085", edgecolor="white", linewidth=0.8, zorder=6)
    ax.annotate(
        "Estados Unidos\n(país mais próximo)", (ux, uy), xytext=(12, 22),
        textcoords="offset points", fontsize=7.8, weight="bold", color="#667085",
        bbox=dict(facecolor=FUNDO, edgecolor="none", alpha=0.9, pad=1.2), zorder=7,
    )
    ax.text(
        (mx + ux) / 2 + 0.05, (my + uy) / 2,
        f"d={distancia_eua:.2f}".replace(".", ","), fontsize=7.3, color=MARITACA,
        va="center", ha="left", zorder=7,
    )

    ax.set_xlim(-1.72, 3.88)
    ax.set_ylim(-2.05, 1.95)
    ax.set_title(
        "Ponto do Sabiá-4 = média de dez formulações genéricas; círculos = formulações individuais",
        loc="left", fontsize=11.2, color="#273142", pad=12,
    )

    legenda = [
        Line2D([0], [0], marker="o", color="none", markerfacecolor="#8E98A5", markeredgecolor="white", markersize=8, label="107 países — IVS"),
        Line2D([0], [0], marker="*", color="none", markerfacecolor=base.CORES["Rio Grande do Sul"], markeredgecolor="white", markersize=14, label="RS — estimativa exploratória"),
        Line2D([0], [0], marker="D", color="none", markerfacecolor=GPT, markeredgecolor="white", markersize=8, label="GPTs — artigo, prompts em inglês"),
        Line2D([0], [0], marker="o", color="none", markerfacecolor=FUNDO, markeredgecolor=MARITACA, markersize=7, label="Sabiá-4 — cada formulação"),
        Line2D([0], [0], marker="H", color="none", markerfacecolor=MARITACA, markeredgecolor="white", markersize=10, label="Sabiá-4 — média"),
    ]
    fig.legend(
        handles=legenda, loc="upper center", bbox_to_anchor=(0.5, 0.885),
        ncol=5, frameon=False, fontsize=8.5,
    )
    fig.suptitle(
        "Mapa cultural: 107 países, o Pampa, GPTs e Sabiá-4",
        x=0.052, y=0.986, ha="left", fontsize=19, weight="bold", color="#182230",
    )
    fig.text(
        0.053, 0.944,
        "Sabiá-4 testado em português em 13 jul. 2026; temperatura zero.",
        ha="left", va="top", fontsize=10.0, color="#4B5563",
    )
    fig.text(
        0.053, 0.018,
        (
            "Fontes: países e GPTs — Tao et al. (2024), OSF 7sj3w; RS — WVS 7 v6.0, Brasil 2018 "
            "(n=118 completos; elipse de bootstrap simples). Sabiá-4 — experimento próprio via Maritaca API, "
            "10 perguntas × 10 descritores traduzidos. Comparação GPT–Sabiá também varia idioma, época e fornecedor."
        ),
        ha="left", va="bottom", fontsize=7.9, color="#5F6875",
    )
    fig.subplots_adjust(top=0.815, bottom=0.115, left=0.085, right=0.975)

    for ext, kwargs in [("png", {"dpi": 260}), ("svg", {}), ("pdf", {})]:
        fig.savefig(
            ROOT / f"figura-mapa-cultural-pampa-ias-maritaca.{ext}",
            bbox_inches="tight", facecolor=fig.get_facecolor(), **kwargs,
        )
    plt.close(fig)


def main() -> None:
    beta, residuo = base.inferir_transformacao()
    if residuo > 1e-10:
        raise RuntimeError(f"Transformação não recuperada com precisão: {residuo:g}")
    variantes, media = calcular_maritaca(beta)
    dados = montar_dados(beta, variantes, media)
    dados.to_csv(ROOT / "coordenadas-mapa-cultural-com-maritaca.csv", index=False)
    variantes.to_csv(ROOT / "coordenadas-maritaca-sabia4-variantes.csv", index=False)
    gerar_figura(dados, variantes, media)

    paises = dados[dados["entity_type"] == "country_human"].copy()
    paises["distance_to_sabia4"] = np.hypot(
        paises["x_survival_self_expression"] - media["x_survival_self_expression"],
        paises["y_traditional_secular"] - media["y_traditional_secular"],
    )
    proximos = paises.nsmallest(5, "distance_to_sabia4")[["entity", "distance_to_sabia4"]]
    destaques = dados[dados["entity"].isin(["Argentina", "Brazil", "Uruguay", "Rio Grande do Sul"])].copy()
    destaques["distance_to_sabia4"] = np.hypot(
        destaques["x_survival_self_expression"] - media["x_survival_self_expression"],
        destaques["y_traditional_secular"] - media["y_traditional_secular"],
    )
    print(f"Sabiá-4: ({media.iloc[0]:.6f}, {media.iloc[1]:.6f})")
    print("Países mais próximos:")
    print(proximos.to_string(index=False))
    print("Distâncias em destaque:")
    print(destaques[["entity", "distance_to_sabia4"]].to_string(index=False))


if __name__ == "__main__":
    main()
