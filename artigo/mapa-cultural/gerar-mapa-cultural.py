#!/usr/bin/env python3
"""Reproduz o mapa cultural de Tao et al. (2024) e acrescenta o RS.

Sem argumentos, usa o ponto do RS já calculado a partir do WVS 7 v6.0.
Para recalculá-lo a partir de uma cópia oficial da microbase:

    python gerar-mapa-cultural.py --wvs /caminho/WVS_Cross-National_Wave_7_csv_v6_0.zip

O script nunca grava nem redistribui a microbase do WVS; exporta apenas
coordenadas agregadas e as figuras.
"""

from __future__ import annotations

import argparse
import math
import os
import zipfile
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib-cache")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D
from matplotlib.patches import Ellipse
from scipy.stats import chi2


ROOT = Path(__file__).resolve().parent
FONTES = ROOT / "fontes"
ITENS = [
    "a008",
    "a165",
    "e018",
    "e025",
    "f063",
    "f118",
    "f120",
    "g006",
    "y002",
    "y003",
]

# Resultado obtido com WVS 7 v6.0, Brasil 2018, N_REGION_ISO = 76021.
# Bootstrap simples de 20.000 reamostragens, seed 20260713.
RS_PRECALCULADO = {
    "x": 0.26588225,
    "y": 0.39769930,
    "x_weighted": 0.28862656,
    "y_weighted": 0.42412690,
    "n_raw": 151,
    "n_complete": 118,
    "ci_x_low": 0.00653452,
    "ci_x_high": 0.53605288,
    "ci_y_low": 0.13697122,
    "ci_y_high": 0.66309311,
    "cov_xx": 0.01839831,
    "cov_xy": -0.00059246,
    "cov_yy": 0.01820301,
}


def inferir_transformacao() -> tuple[np.ndarray, float]:
    """Recupera a transformação afim usada no artigo a partir da replicação OSF.

    A pontuação de componentes é linear. As médias das dez respostas do GPT-4o
    culturalmente condicionado, combinadas às coordenadas publicadas, identificam
    exatamente o intercepto e os dez coeficientes de cada eixo.
    """

    respostas = pd.read_csv(FONTES / "localized_gpt4o_answers.csv")
    coords = pd.read_csv(FONTES / "coordinates_human_gpt4o.csv")
    medias = respostas.groupby("country", as_index=False)[ITENS].mean()
    treino = medias.merge(
        coords,
        left_on="country",
        right_on="country.territory",
        how="inner",
        validate="one_to_one",
    )
    x = np.column_stack([np.ones(len(treino)), treino[ITENS].to_numpy(float)])
    y = treino[["RC1_cp_gpt_4o", "RC2_cp_gpt_4o"]].to_numpy(float)
    beta, *_ = np.linalg.lstsq(x, y, rcond=None)
    max_residuo = float(np.max(np.abs(x @ beta - y)))
    return beta, max_residuo


def pontuar(media_itens: np.ndarray, beta: np.ndarray) -> np.ndarray:
    return np.r_[1.0, np.asarray(media_itens, dtype=float)] @ beta


def pontos_ias(beta: np.ndarray) -> pd.DataFrame:
    arquivos = [
        ("GPT-3.5", "gpt-3.5-turbo-0613", "default_gpt35_answers.csv"),
        ("GPT-4", "gpt-4-0613", "default_gpt4_answers.csv"),
        ("GPT-4 Turbo", "gpt-4-turbo-2024-04-09", "default_gpt4turbo_answers.csv"),
        ("GPT-4o", "gpt-4o-2024-05-13", "default_gpt4o_answers.csv"),
    ]
    linhas = []
    for rotulo, versao, arquivo in arquivos:
        respostas = pd.read_csv(FONTES / arquivo)
        xy = pontuar(respostas[ITENS].mean().to_numpy(float), beta)
        linhas.append(
            {
                "entity": rotulo,
                "entity_type": "ai_default",
                "model_version": versao,
                "reference_entity": "",
                "x_survival_self_expression": xy[0],
                "y_traditional_secular": xy[1],
            }
        )

    # O artigo usou apenas uma formulação de prompt para o GPT-3.
    gpt3 = np.array([2, 1, 1, 1, 7, 6, 5, 2, 2, 1], dtype=float)
    xy = pontuar(gpt3, beta)
    linhas.append(
        {
            "entity": "GPT-3",
            "entity_type": "ai_default",
            "model_version": "text-davinci-002",
            "reference_entity": "",
            "x_survival_self_expression": xy[0],
            "y_traditional_secular": xy[1],
        }
    )
    return pd.DataFrame(linhas)


def _ler_wvs(caminho: Path, usecols: set[str]) -> pd.DataFrame:
    seletor = lambda c: c in usecols
    if caminho.suffix.lower() == ".zip":
        with zipfile.ZipFile(caminho) as zf:
            csvs = [i for i in zf.infolist() if i.filename.lower().endswith(".csv")]
            if not csvs:
                raise ValueError("O ZIP informado não contém arquivo CSV.")
            alvo = max(csvs, key=lambda i: i.file_size)
            with zf.open(alvo) as fh:
                return pd.read_csv(fh, usecols=seletor, low_memory=False)
    return pd.read_csv(caminho, usecols=seletor, low_memory=False)


def calcular_rs(caminho_wvs: Path, beta: np.ndarray) -> dict[str, float]:
    colunas = {
        "B_COUNTRY",
        "N_REGION_ISO",
        "N_REGION_WVS",
        "W_WEIGHT",
        "Q46",
        "Q57",
        "Q45",
        "Q209",
        "Q164",
        "Q182",
        "Q184",
        "Q254",
        "Y002",
        "Y003",
    }
    dados = _ler_wvs(caminho_wvs, colunas)
    if "B_COUNTRY" not in dados:
        raise ValueError("A microbase não contém B_COUNTRY.")

    brasil = dados[dados["B_COUNTRY"] == 76].copy()
    if "N_REGION_ISO" in brasil and (brasil["N_REGION_ISO"] == 76021).any():
        rs = brasil[brasil["N_REGION_ISO"] == 76021].copy()
    elif "N_REGION_WVS" in brasil and (brasil["N_REGION_WVS"] == 76058).any():
        rs = brasil[brasil["N_REGION_WVS"] == 76058].copy()
    else:
        raise ValueError("Não foi possível localizar BR-RS (76021/76058) na microbase.")

    n_raw = len(rs)
    rs = rs.rename(
        columns={
            "Q46": "a008",
            "Q57": "a165",
            "Q45": "e018",
            "Q209": "e025",
            "Q164": "f063",
            "Q182": "f118",
            "Q184": "f120",
            "Q254": "g006",
            "Y002": "y002",
            "Y003": "y003",
        }
    )
    for item in ITENS[:-1]:
        rs.loc[rs[item] <= 0, item] = np.nan
    # Replica literalmente a regra de Tao et al.: Y003 > -5 é válido.
    rs.loc[rs["y003"] <= -5, "y003"] = np.nan
    completos = rs.dropna(subset=ITENS).copy()
    if completos.empty:
        raise ValueError("Nenhum caso completo do RS nos dez itens do mapa.")

    matriz = np.column_stack(
        [np.ones(len(completos)), completos[ITENS].to_numpy(float)]
    )
    scores = matriz @ beta
    centro = scores.mean(axis=0)

    if "W_WEIGHT" in completos and (completos["W_WEIGHT"] > 0).any():
        pesos = completos["W_WEIGHT"].to_numpy(float)
        ponderado = np.average(scores, axis=0, weights=pesos)
    else:
        ponderado = np.array([np.nan, np.nan])

    rng = np.random.default_rng(20260713)
    n = len(scores)
    indices = rng.integers(0, n, size=(20_000, n))
    boot = scores[indices].mean(axis=1)
    cov = np.cov(boot.T)
    qx = np.quantile(boot[:, 0], [0.025, 0.975])
    qy = np.quantile(boot[:, 1], [0.025, 0.975])
    return {
        "x": float(centro[0]),
        "y": float(centro[1]),
        "x_weighted": float(ponderado[0]),
        "y_weighted": float(ponderado[1]),
        "n_raw": int(n_raw),
        "n_complete": int(n),
        "ci_x_low": float(qx[0]),
        "ci_x_high": float(qx[1]),
        "ci_y_low": float(qy[0]),
        "ci_y_high": float(qy[1]),
        "cov_xx": float(cov[0, 0]),
        "cov_xy": float(cov[0, 1]),
        "cov_yy": float(cov[1, 1]),
    }


def montar_dados(beta: np.ndarray, rs: dict[str, float]) -> pd.DataFrame:
    fonte = pd.read_csv(FONTES / "coordinates_human_gpt4o.csv")
    paises = pd.DataFrame(
        {
            "entity": fonte["country.territory"],
            "entity_type": "country_human",
            "model_version": "",
            "reference_entity": "",
            "x_survival_self_expression": fonte["RC1_human_survey"],
            "y_traditional_secular": fonte["RC2_human_survey"],
            "n_raw": np.nan,
            "n_complete": np.nan,
            "ci95_x_low": np.nan,
            "ci95_x_high": np.nan,
            "ci95_y_low": np.nan,
            "ci95_y_high": np.nan,
            "source": "Tao et al. (2024), OSF 7sj3w",
            "notes": "Média das coordenadas país-ano nas ondas 5–7 do IVS.",
        }
    )

    ias = pontos_ias(beta)
    for coluna in [
        "n_raw",
        "n_complete",
        "ci95_x_low",
        "ci95_x_high",
        "ci95_y_low",
        "ci95_y_high",
    ]:
        ias[coluna] = np.nan
    ias["source"] = "Tao et al. (2024), replicação OSF 7sj3w"
    ias["notes"] = "Expressão cultural padrão; versões históricas avaliadas no artigo."

    # Pontos do GPT-4o quando instruído a responder como pessoa típica do país.
    prompts = fonte[fonte["country.territory"].isin(["Argentina", "Brazil", "Uruguay"])].copy()
    prompts = pd.DataFrame(
        {
            "entity": "GPT-4o — prompt " + prompts["country.territory"],
            "entity_type": "ai_cultural_prompt",
            "model_version": "gpt-4o-2024-05-13",
            "reference_entity": prompts["country.territory"],
            "x_survival_self_expression": prompts["RC1_cp_gpt_4o"],
            "y_traditional_secular": prompts["RC2_cp_gpt_4o"],
            "n_raw": np.nan,
            "n_complete": np.nan,
            "ci95_x_low": np.nan,
            "ci95_x_high": np.nan,
            "ci95_y_low": np.nan,
            "ci95_y_high": np.nan,
            "source": "Tao et al. (2024), OSF 7sj3w",
            "notes": "Média de dez variantes de prompt cultural por país.",
        }
    )

    linha_rs = pd.DataFrame(
        [
            {
                "entity": "Rio Grande do Sul",
                "entity_type": "regional_human_exploratory",
                "model_version": "",
                "reference_entity": "Brazil",
                "x_survival_self_expression": rs["x"],
                "y_traditional_secular": rs["y"],
                "n_raw": rs["n_raw"],
                "n_complete": rs["n_complete"],
                "ci95_x_low": rs["ci_x_low"],
                "ci95_x_high": rs["ci_x_high"],
                "ci95_y_low": rs["ci_y_low"],
                "ci95_y_high": rs["ci_y_high"],
                "source": "Cálculo exploratório; WVS 7 v6.0, Brasil 2018",
                "notes": (
                    "Média não ponderada para compatibilidade com Tao et al.; "
                    f"sensibilidade ponderada=({rs['x_weighted']:.6f}, {rs['y_weighted']:.6f})."
                ),
            }
        ]
    )
    return pd.concat([paises, linha_rs, ias, prompts], ignore_index=True)


CORES = {
    "Argentina": "#2563EB",
    "Brazil": "#16A34A",
    "Uruguay": "#D97706",
    "Rio Grande do Sul": "#DC2626",
}
ROTULOS = {
    "Argentina": "Argentina",
    "Brazil": "Brasil",
    "Uruguay": "Uruguai",
    "Rio Grande do Sul": "Rio Grande do Sul",
}


def adicionar_elipse(ax: plt.Axes, rs: dict[str, float]) -> None:
    cov = np.array(
        [[rs["cov_xx"], rs["cov_xy"]], [rs["cov_xy"], rs["cov_yy"]]],
        dtype=float,
    )
    valores, vetores = np.linalg.eigh(cov)
    ordem = valores.argsort()[::-1]
    valores, vetores = valores[ordem], vetores[:, ordem]
    angulo = math.degrees(math.atan2(vetores[1, 0], vetores[0, 0]))
    escala = math.sqrt(chi2.ppf(0.95, df=2))
    largura, altura = 2 * escala * np.sqrt(valores)
    ax.add_patch(
        Ellipse(
            (rs["x"], rs["y"]),
            width=largura,
            height=altura,
            angle=angulo,
            facecolor=CORES["Rio Grande do Sul"],
            edgecolor=CORES["Rio Grande do Sul"],
            alpha=0.10,
            linewidth=1.4,
            zorder=2,
        )
    )


def estilo_eixos(ax: plt.Axes) -> None:
    ax.set_facecolor("#FCFBF8")
    ax.grid(True, color="#D8DDE4", linewidth=0.7, alpha=0.65)
    ax.axhline(0, color="#8B95A5", linewidth=0.9, alpha=0.75)
    ax.axvline(0, color="#8B95A5", linewidth=0.9, alpha=0.75)
    for lado in ["top", "right"]:
        ax.spines[lado].set_visible(False)
    ax.spines["left"].set_color("#8B95A5")
    ax.spines["bottom"].set_color("#8B95A5")
    ax.tick_params(colors="#4B5563", labelsize=8.5)
    ax.set_xlabel(
        "Sobrevivência  ←    eixo 1    →  Autoexpressão",
        fontsize=10,
        color="#273142",
    )
    ax.set_ylabel(
        "Tradicionais  ←    eixo 2    →  Seculares-racionais",
        fontsize=10,
        color="#273142",
    )


def gerar_figura(dados: pd.DataFrame, rs: dict[str, float]) -> None:
    paises = dados[dados["entity_type"] == "country_human"]
    ias = dados[dados["entity_type"] == "ai_default"]
    regionais = dados[
        dados["entity"].isin(["Argentina", "Brazil", "Uruguay", "Rio Grande do Sul"])
    ]
    prompts = dados[dados["entity_type"] == "ai_cultural_prompt"]

    plt.rcParams.update({"font.family": "DejaVu Sans", "axes.titleweight": "bold"})
    fig, (ax, ax2) = plt.subplots(
        1,
        2,
        figsize=(15.5, 8.2),
        gridspec_kw={"width_ratios": [1.28, 1.0], "wspace": 0.18},
        facecolor="#FCFBF8",
    )
    estilo_eixos(ax)
    estilo_eixos(ax2)

    # Painel A: os 107 países, RS e as cinco versões históricas.
    ax.scatter(
        paises["x_survival_self_expression"],
        paises["y_traditional_secular"],
        s=25,
        color="#A8B0BB",
        alpha=0.68,
        edgecolor="white",
        linewidth=0.35,
        zorder=1,
    )
    contexto = {
        "United States": (4, -10),
        "Sweden": (4, 5),
        "Germany": (4, 5),
        "Japan": (4, 5),
        "China": (4, 5),
        "Russia": (4, 5),
        "India": (4, -10),
        "Nigeria": (4, -10),
        "South Africa": (4, 5),
        "Australia": (4, -10),
    }
    for nome, deslocamento in contexto.items():
        linha = paises[paises["entity"] == nome]
        if linha.empty:
            continue
        x, y = linha.iloc[0][
            ["x_survival_self_expression", "y_traditional_secular"]
        ]
        ax.annotate(
            nome,
            (x, y),
            xytext=deslocamento,
            textcoords="offset points",
            fontsize=6.5,
            color="#7B8491",
            alpha=0.9,
            zorder=2,
        )

    adicionar_elipse(ax, rs)
    offsets_regiao = {
        "Argentina": (7, 7),
        "Brazil": (-43, -15),
        "Uruguay": (7, -14),
        "Rio Grande do Sul": (7, 8),
    }
    for _, linha in regionais.iterrows():
        nome = linha["entity"]
        marcador = "*" if nome == "Rio Grande do Sul" else "o"
        tamanho = 220 if marcador == "*" else 105
        ax.scatter(
            linha["x_survival_self_expression"],
            linha["y_traditional_secular"],
            s=tamanho,
            marker=marcador,
            color=CORES[nome],
            edgecolor="white",
            linewidth=1.1,
            zorder=5,
        )
        ax.annotate(
            ROTULOS[nome] + (" (2018)" if nome == "Rio Grande do Sul" else ""),
            (linha["x_survival_self_expression"], linha["y_traditional_secular"]),
            xytext=offsets_regiao[nome],
            textcoords="offset points",
            fontsize=8.5,
            weight="bold",
            color=CORES[nome],
            bbox=dict(facecolor="#FCFBF8", edgecolor="none", alpha=0.88, pad=1.4),
            zorder=6,
        )

    ax.scatter(
        ias["x_survival_self_expression"],
        ias["y_traditional_secular"],
        s=100,
        marker="D",
        facecolor="#7C3AED",
        edgecolor="white",
        linewidth=1.0,
        zorder=6,
    )
    offsets_ia = {
        "GPT-3": (8, -4),
        "GPT-3.5": (-2, 10),
        "GPT-4": (8, 7),
        "GPT-4 Turbo": (8, -10),
        "GPT-4o": (-40, 9),
    }
    for _, linha in ias.iterrows():
        ax.annotate(
            linha["entity"],
            (linha["x_survival_self_expression"], linha["y_traditional_secular"]),
            xytext=offsets_ia[linha["entity"]],
            textcoords="offset points",
            fontsize=8.2,
            weight="bold",
            color="#6D28D9",
            bbox=dict(facecolor="#FCFBF8", edgecolor="none", alpha=0.88, pad=1.2),
            zorder=7,
        )
    ax.set_xlim(-1.70, 3.82)
    ax.set_ylim(-1.78, 1.92)
    ax.set_title("A  |  107 países + RS + expressões padrão das IAs", loc="left", fontsize=12)

    # Painel B: distância entre humanos e GPT-4o com prompt cultural.
    ax2.scatter(
        paises["x_survival_self_expression"],
        paises["y_traditional_secular"],
        s=18,
        color="#C7CDD5",
        alpha=0.28,
        edgecolor="none",
        zorder=1,
    )
    adicionar_elipse(ax2, rs)
    for _, linha in regionais.iterrows():
        nome = linha["entity"]
        marcador = "*" if nome == "Rio Grande do Sul" else "o"
        ax2.scatter(
            linha["x_survival_self_expression"],
            linha["y_traditional_secular"],
            s=210 if marcador == "*" else 100,
            marker=marcador,
            color=CORES[nome],
            edgecolor="white",
            linewidth=1.0,
            zorder=5,
        )

    nomes_prompt = {"Argentina": "Argentina", "Brazil": "Brasil", "Uruguay": "Uruguai"}
    offsets_b = {"Argentina": (-16, 9), "Brazil": (-30, -17), "Uruguay": (-8, -17)}
    for chave, rotulo in nomes_prompt.items():
        humano = regionais[regionais["entity"] == chave].iloc[0]
        ia = prompts[prompts["reference_entity"] == chave].iloc[0]
        hx, hy = humano[["x_survival_self_expression", "y_traditional_secular"]]
        ix, iy = ia[["x_survival_self_expression", "y_traditional_secular"]]
        ax2.annotate(
            "",
            xy=(ix, iy),
            xytext=(hx, hy),
            arrowprops=dict(
                arrowstyle="-|>",
                color=CORES[chave],
                linewidth=1.4,
                linestyle=(0, (4, 3)),
                alpha=0.82,
            ),
            zorder=3,
        )
        ax2.scatter(
            ix,
            iy,
            s=105,
            marker="D",
            facecolor="#FCFBF8",
            edgecolor=CORES[chave],
            linewidth=1.8,
            zorder=6,
        )
        distancia = float(np.hypot(ix - hx, iy - hy))
        ax2.text(
            (hx + ix) / 2,
            (hy + iy) / 2 + 0.045,
            f"d={distancia:.2f}".replace(".", ","),
            fontsize=7.3,
            color=CORES[chave],
            ha="center",
            va="bottom",
            bbox=dict(facecolor="#FCFBF8", edgecolor="none", alpha=0.78, pad=0.8),
            zorder=7,
        )
        ax2.annotate(
            rotulo,
            (hx, hy),
            xytext=offsets_b[chave],
            textcoords="offset points",
            fontsize=8.2,
            weight="bold",
            color=CORES[chave],
            zorder=7,
        )
        ax2.annotate(
            "GPT-4o\ncom prompt",
            (ix, iy),
            xytext=(6, 5),
            textcoords="offset points",
            fontsize=7.2,
            color=CORES[chave],
            zorder=7,
        )

    ax2.annotate(
        "RS (estimativa humana)\nsem prompt subnacional no estudo",
        (rs["x"], rs["y"]),
        xytext=(8, 9),
        textcoords="offset points",
        fontsize=8.0,
        weight="bold",
        color=CORES["Rio Grande do Sul"],
        bbox=dict(facecolor="#FCFBF8", edgecolor="none", alpha=0.88, pad=1.2),
        zorder=7,
    )
    ax2.set_xlim(-0.45, 3.18)
    ax2.set_ylim(-1.00, 0.86)
    ax2.set_title("B  |  O prompt cultural reduz, mas não elimina, a distância", loc="left", fontsize=12)

    legenda = [
        Line2D([0], [0], marker="o", color="none", markerfacecolor="#6B7280", markeredgecolor="white", markersize=8, label="Pesquisa com humanos"),
        Line2D([0], [0], marker="*", color="none", markerfacecolor=CORES["Rio Grande do Sul"], markeredgecolor="white", markersize=13, label="RS (estimativa exploratória)"),
        Line2D([0], [0], marker="D", color="none", markerfacecolor="#7C3AED", markeredgecolor="white", markersize=8, label="IA — expressão padrão"),
        Line2D([0], [0], marker="D", color="none", markerfacecolor="#FCFBF8", markeredgecolor="#6B7280", markersize=8, label="GPT-4o — prompt cultural"),
    ]
    fig.legend(
        handles=legenda,
        loc="upper center",
        bbox_to_anchor=(0.5, 0.905),
        ncol=4,
        frameon=False,
        fontsize=8.5,
    )
    fig.suptitle(
        "Mapa cultural: 107 países, o Pampa e cinco versões históricas de GPT",
        x=0.045,
        y=0.985,
        ha="left",
        fontsize=18,
        weight="bold",
        color="#182230",
    )
    fig.text(
        0.046,
        0.945,
        "O ponto do Rio Grande do Sul é uma extensão exploratória da metodologia do artigo; Argentina e Uruguai são médias nacionais.",
        ha="left",
        va="top",
        fontsize=9.5,
        color="#4B5563",
    )
    fig.text(
        0.046,
        0.018,
        (
            "Fontes: Tao et al. (2024) e replicação OSF; WVS 7 v6.0 para RS. "
            "Países = médias país-ano das ondas 5–7; RS = Brasil 2018, n=118 casos completos (151 entrevistados). "
            "Elipse = bootstrap simples de respondentes, sem ajuste ao desenho amostral. IAs = versões avaliadas em 2020–2024."
        ),
        ha="left",
        va="bottom",
        fontsize=7.6,
        color="#5F6875",
    )
    fig.subplots_adjust(top=0.835, bottom=0.105, left=0.07, right=0.985)

    for extensao, kwargs in [
        ("png", {"dpi": 240}),
        ("svg", {}),
        ("pdf", {}),
    ]:
        fig.savefig(
            ROOT / f"figura-mapa-cultural-pampa-ia.{extensao}",
            bbox_inches="tight",
            facecolor=fig.get_facecolor(),
            **kwargs,
        )
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--wvs",
        type=Path,
        help="CSV ou ZIP oficial WVS 7 v6.0 para recalcular o ponto do RS.",
    )
    args = parser.parse_args()
    beta, residuo = inferir_transformacao()
    if residuo > 1e-10:
        raise RuntimeError(f"Transformação não recuperada com precisão: {residuo:g}")
    rs = calcular_rs(args.wvs, beta) if args.wvs else dict(RS_PRECALCULADO)
    dados = montar_dados(beta, rs)
    dados.to_csv(ROOT / "coordenadas-mapa-cultural.csv", index=False, encoding="utf-8")
    gerar_figura(dados, rs)

    coef = pd.DataFrame(
        beta,
        index=["intercepto", *ITENS],
        columns=["eixo_1_sobrevivencia_autoexpressao", "eixo_2_tradicional_secular"],
    )
    coef.to_csv(ROOT / "coeficientes-transformacao.csv", encoding="utf-8")
    print(
        f"RS: ({rs['x']:.6f}, {rs['y']:.6f}); "
        f"n={rs['n_complete']}/{rs['n_raw']}; resíduo máximo={residuo:.2e}"
    )


if __name__ == "__main__":
    main()
