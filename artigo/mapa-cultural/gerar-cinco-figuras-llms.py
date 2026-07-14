#!/usr/bin/env python3
"""Gera quatro mapas por condição e um mapa combinado de trajetórias.

As figuras preservam os 107 países, destacam Brasil, Argentina, Uruguai e
Rio Grande do Sul e removem elipses/anéis de alvo. Nas figuras separadas,
os pontos translúcidos representam formulações completas; no mapa combinado,
somente os pontos centrais são mostrados e ligados na ordem 1–2–3–4.
"""

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
MULTI_PATH = ROOT / "gerar-mapa-cultural-llms-multicondicao.py"
SPEC = importlib.util.spec_from_file_location("mapa_multi", MULTI_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("Não foi possível carregar o gerador multicondição.")
multi = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(multi)
base = multi.base

FUNDO = "#FCFBF8"
CINZA_PAIS = "#A8B0BB"
CINZA_ROTULO = "#667085"

CONDICOES = {
    "en_default": {
        "numero": 1,
        "titulo": "Mapa cultural — condição 1",
        "subtitulo": "Perguntas e descritores em inglês",
        "slug": "condicao-1-ingles",
    },
    "pt_default": {
        "numero": 2,
        "titulo": "Mapa cultural — condição 2",
        "subtitulo": "Perguntas e descritores em português brasileiro",
        "slug": "condicao-2-portugues",
    },
    "pt_brazil": {
        "numero": 3,
        "titulo": "Mapa cultural — condição 3",
        "subtitulo": "Português brasileiro + identidade brasileira",
        "slug": "condicao-3-identidade-brasileira",
    },
    "pt_rs": {
        "numero": 4,
        "titulo": "Mapa cultural — condição 4",
        "subtitulo": "Português brasileiro + identidade gaúcha",
        "slug": "condicao-4-identidade-gaucha",
    },
}

TRADUCOES_PAISES = {
    "North Ireland": "Irlanda do\nNorte",
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
}

# Deslocamentos manuais mantêm os rótulos legíveis também no mapa combinado.
OFFSETS_PAISES = {
    "North Ireland": (-47, -27),
    "United States": (38, -17),
    "Japan": (7, 7),
    "Germany": (-82, 18),
    "Mongolia": (-52, 8),
    "Slovenia": (7, 7),
    "Vietnam": (-44, -15),
    "Czechia": (-46, 8),
    "Mexico": (-39, -15),
    "Ireland": (7, -15),
    "Spain": (7, 7),
}

OFFSETS_HUMANOS = {
    "Argentina": (7, 7),
    "Brazil": (-41, -15),
    "Uruguay": (7, -15),
    "Rio Grande do Sul": (7, 8),
}


def preparar_dados() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    beta, residuo = base.inferir_transformacao()
    if residuo > 1e-10:
        raise RuntimeError(f"Transformação não recuperada com precisão: {residuo:g}")
    dados_base = base.montar_dados(beta, dict(base.RS_PRECALCULADO))
    variantes, medias = multi.calcular_coordenadas(beta)
    paises = dados_base[dados_base["entity_type"] == "country_human"].copy()
    humanos = dados_base[
        dados_base["entity"].isin(["Argentina", "Brazil", "Uruguay", "Rio Grande do Sul"])
    ].copy()
    if len(paises) != 107 or len(humanos) != 4:
        raise ValueError(f"Base humana inesperada: {len(paises)=}, {len(humanos)=}")
    return paises, humanos, variantes, medias


def paises_proximos(
    paises: pd.DataFrame,
    medias: pd.DataFrame,
) -> dict[tuple[str, str], str]:
    """País não destacado mais próximo de cada modelo-condição.

    Brasil, Argentina e Uruguai já têm rótulos coloridos próprios; quando um
    deles é o vizinho absoluto, rotulamos em cinza o país seguinte para evitar
    duplicação visual e ainda oferecer contexto geográfico ao ponto do modelo.
    """

    candidatos = paises[~paises["entity"].isin(["Argentina", "Brazil", "Uruguay"])]
    resultado: dict[tuple[str, str], str] = {}
    for _, modelo in medias.iterrows():
        distancias = np.hypot(
            candidatos["x_survival_self_expression"]
            - modelo["x_survival_self_expression"],
            candidatos["y_traditional_secular"] - modelo["y_traditional_secular"],
        )
        resultado[(modelo["model_label"], modelo["condition"])] = str(
            candidatos.loc[distancias.idxmin(), "entity"]
        )
    return resultado


def limites_variantes(
    paises: pd.DataFrame,
    variantes: pd.DataFrame,
) -> tuple[tuple[float, float], tuple[float, float]]:
    xs = pd.concat([paises["x_survival_self_expression"], variantes["x_survival_self_expression"]])
    ys = pd.concat([paises["y_traditional_secular"], variantes["y_traditional_secular"]])
    return (
        (min(-1.72, float(xs.min()) - 0.25), max(3.90, float(xs.max()) + 0.25)),
        (min(-2.10, float(ys.min()) - 0.25), max(2.05, float(ys.max()) + 0.25)),
    )


def desenhar_base(
    ax: plt.Axes,
    paises: pd.DataFrame,
    humanos: pd.DataFrame,
    nomes_cinza: set[str],
) -> None:
    base.estilo_eixos(ax)
    ax.scatter(
        paises["x_survival_self_expression"],
        paises["y_traditional_secular"],
        s=28,
        color=CINZA_PAIS,
        alpha=0.67,
        edgecolor="white",
        linewidth=0.35,
        zorder=1,
    )

    for nome in sorted(nomes_cinza):
        linha = paises[paises["entity"] == nome]
        if linha.empty:
            continue
        x = float(linha.iloc[0]["x_survival_self_expression"])
        y = float(linha.iloc[0]["y_traditional_secular"])
        ax.scatter([x], [y], s=31, color="#8E98A5", edgecolor="white", linewidth=0.4, zorder=2)
        ax.annotate(
            TRADUCOES_PAISES.get(nome, nome),
            (x, y),
            xytext=OFFSETS_PAISES.get(nome, (6, 6)),
            textcoords="offset points",
            fontsize=8.0,
            color=CINZA_ROTULO,
            weight="semibold",
            bbox=dict(facecolor=FUNDO, edgecolor="none", alpha=0.88, pad=0.8),
            zorder=5,
        )

    # Apenas os pontos sólidos: nenhuma elipse, halo ou anel de alvo.
    for _, linha in humanos.iterrows():
        nome = str(linha["entity"])
        marcador = "*" if nome == "Rio Grande do Sul" else "o"
        ax.scatter(
            linha["x_survival_self_expression"],
            linha["y_traditional_secular"],
            s=185 if marcador == "*" else 95,
            marker=marcador,
            color=base.CORES[nome],
            edgecolor="white",
            linewidth=1.0,
            zorder=7,
        )
        ax.annotate(
            base.ROTULOS[nome],
            (linha["x_survival_self_expression"], linha["y_traditional_secular"]),
            xytext=OFFSETS_HUMANOS[nome],
            textcoords="offset points",
            fontsize=8.7,
            weight="bold",
            color=base.CORES[nome],
            bbox=dict(facecolor=FUNDO, edgecolor="none", alpha=0.91, pad=0.9),
            zorder=8,
        )


def legenda_modelos(incluir_variantes: bool) -> list[Line2D]:
    itens = [
        Line2D(
            [0], [0], marker=estilo["marker"], color="none",
            markerfacecolor=estilo["color"], markeredgecolor="white",
            markersize=9, label=estilo["short"],
        )
        for estilo in multi.MODELOS.values()
    ]
    itens.append(
        Line2D(
            [0], [0], marker="o", color="none", markerfacecolor="#8E98A5",
            markeredgecolor="white", markersize=7.5, label="107 países — IVS",
        )
    )
    if incluir_variantes:
        itens.append(
            Line2D(
                [0], [0], marker="o", color="none", markerfacecolor="#667085",
                markeredgecolor="none", alpha=0.28, markersize=6.5,
                label="Formulações completas",
            )
        )
    return itens


def salvar(fig: plt.Figure, nome: str) -> None:
    for ext, kwargs in [("png", {"dpi": 260}), ("svg", {}), ("pdf", {})]:
        fig.savefig(
            ROOT / f"{nome}.{ext}",
            bbox_inches="tight",
            facecolor=fig.get_facecolor(),
            **kwargs,
        )
    plt.close(fig)


def gerar_separadas(
    paises: pd.DataFrame,
    humanos: pd.DataFrame,
    variantes: pd.DataFrame,
    medias: pd.DataFrame,
    vizinhos: dict[tuple[str, str], str],
) -> None:
    for condicao, info in CONDICOES.items():
        fig, ax = plt.subplots(figsize=(13.9, 8.6), facecolor=FUNDO)
        variantes_condicao = variantes[variantes["condition"] == condicao]
        xlim, ylim = limites_variantes(paises, variantes_condicao)
        nomes = {
            vizinhos[(modelo, condicao)]
            for modelo in multi.MODELOS
        }
        desenhar_base(ax, paises, humanos, nomes)

        for modelo, estilo in multi.MODELOS.items():
            pontos = variantes[
                (variantes["condition"] == condicao)
                & (variantes["model_label"] == modelo)
            ]
            media = medias[
                (medias["condition"] == condicao)
                & (medias["model_label"] == modelo)
            ].iloc[0]
            ax.scatter(
                pontos["x_survival_self_expression"],
                pontos["y_traditional_secular"],
                s=34,
                marker="o",
                facecolor=estilo["color"],
                edgecolor="none",
                alpha=0.22,
                zorder=3,
            )
            ax.scatter(
                [media["x_survival_self_expression"]],
                [media["y_traditional_secular"]],
                s=165,
                marker=estilo["marker"],
                facecolor=estilo["color"],
                edgecolor="white",
                linewidth=1.1,
                zorder=9,
            )

        ax.set_xlim(*xlim)
        ax.set_ylim(*ylim)
        fig.suptitle(
            info["titulo"], x=0.055, y=0.985, ha="left",
            fontsize=20, weight="bold", color="#182230",
        )
        fig.text(
            0.056, 0.943,
            f"{info['subtitulo']}; cinco LLMs comparados a 107 países.",
            ha="left", va="top", fontsize=10.5, color="#4B5563",
        )
        fig.legend(
            handles=legenda_modelos(incluir_variantes=True),
            loc="upper center", bbox_to_anchor=(0.5, 0.895), ncol=7,
            frameon=False, fontsize=8.8, columnspacing=1.15, handletextpad=0.45,
        )
        fig.text(
            0.056, 0.018,
            (
                "Nomes em cinza: país não destacado mais próximo de cada LLM. "
                "Fontes: países — Tao et al. (2024), OSF 7sj3w; RS — WVS 7 v6.0, Brasil 2018, n=118; "
                "LLMs — experimento próprio, jul. 2026."
            ),
            ha="left", va="bottom", fontsize=7.8, color="#5F6875",
        )
        fig.subplots_adjust(top=0.805, bottom=0.115, left=0.083, right=0.982)
        salvar(fig, f"figura-mapa-cultural-{info['slug']}")


def gerar_combinada(
    paises: pd.DataFrame,
    humanos: pd.DataFrame,
    medias: pd.DataFrame,
    vizinhos: dict[tuple[str, str], str],
) -> None:
    fig, ax = plt.subplots(figsize=(14.7, 9.0), facecolor=FUNDO)
    nomes = set(vizinhos.values())
    desenhar_base(ax, paises, humanos, nomes)

    ordem = list(CONDICOES)
    offsets_numeros = {
        "en_default": (-10, 8),
        "pt_default": (7, 8),
        "pt_brazil": (7, -13),
        "pt_rs": (-10, -13),
    }
    for modelo, estilo in multi.MODELOS.items():
        trajetoria = (
            medias[medias["model_label"] == modelo]
            .set_index("condition")
            .loc[ordem]
            .reset_index()
        )
        ax.plot(
            trajetoria["x_survival_self_expression"],
            trajetoria["y_traditional_secular"],
            color=estilo["color"],
            linewidth=1.55,
            linestyle=(0, (2.0, 2.6)),
            alpha=0.75,
            zorder=4,
        )
        for _, ponto in trajetoria.iterrows():
            condicao = str(ponto["condition"])
            ax.scatter(
                [ponto["x_survival_self_expression"]],
                [ponto["y_traditional_secular"]],
                s=155,
                marker=estilo["marker"],
                facecolor=estilo["color"],
                edgecolor="white",
                linewidth=1.05,
                zorder=9,
            )
            ax.annotate(
                str(CONDICOES[condicao]["numero"]),
                (ponto["x_survival_self_expression"], ponto["y_traditional_secular"]),
                xytext=offsets_numeros[condicao],
                textcoords="offset points",
                fontsize=8.3,
                weight="bold",
                color=estilo["color"],
                bbox=dict(facecolor=FUNDO, edgecolor="none", alpha=0.9, pad=0.25),
                zorder=10,
            )

    ax.set_xlim(-1.72, 3.90)
    ax.set_ylim(-2.12, 2.20)
    fig.suptitle(
        "Trajetórias linguístico-culturais de cinco LLMs",
        x=0.052, y=0.985, ha="left", fontsize=20, weight="bold", color="#182230",
    )
    fig.text(
        0.053, 0.944,
        "1 inglês  ·  2 português brasileiro  ·  3 identidade brasileira  ·  4 identidade gaúcha",
        ha="left", va="top", fontsize=10.5, color="#4B5563",
    )
    fig.legend(
        handles=legenda_modelos(incluir_variantes=False),
        loc="upper center", bbox_to_anchor=(0.5, 0.895), ncol=6,
        frameon=False, fontsize=9.0, columnspacing=1.35, handletextpad=0.48,
    )
    fig.text(
        0.053, 0.018,
        (
            "Linhas pontilhadas conectam, para cada modelo, as condições 1→2→3→4. "
            "Nomes em cinza: países não destacados mais próximos dos pontos. "
            "Fontes: Tao et al. (2024); WVS 7; experimento próprio, jul. 2026."
        ),
        ha="left", va="bottom", fontsize=7.9, color="#5F6875",
    )
    fig.subplots_adjust(top=0.805, bottom=0.112, left=0.081, right=0.982)
    salvar(fig, "figura-mapa-cultural-quatro-condicoes-trajetorias")


def main() -> None:
    plt.rcParams.update({"font.family": "DejaVu Sans", "axes.titleweight": "bold"})
    paises, humanos, variantes, medias = preparar_dados()
    vizinhos = paises_proximos(paises, medias)
    gerar_separadas(paises, humanos, variantes, medias, vizinhos)
    gerar_combinada(paises, humanos, medias, vizinhos)
    for condicao, info in CONDICOES.items():
        nomes = sorted(
            {vizinhos[(modelo, condicao)] for modelo in multi.MODELOS},
            key=lambda nome: TRADUCOES_PAISES.get(nome, nome),
        )
        print(f"{info['numero']}: " + ", ".join(TRADUCOES_PAISES.get(n, n) for n in nomes))


if __name__ == "__main__":
    main()
