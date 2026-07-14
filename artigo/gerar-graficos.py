"""Reproduz as quatro figuras do banco de evidências.

Os números são transcrições de resultados publicados; veja dados-figuras.csv e
as notas metodológicas no banco-de-evidencias.md.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "figuras"
DATA = pd.read_csv(ROOT / "dados-figuras.csv")

COLORS = {
    "blue": "#365B8C",
    "terracotta": "#C25A3A",
    "teal": "#2A7F62",
    "gold": "#D6A93B",
    "gray": "#85939C",
    "dark": "#263238",
    "light": "#E8EDF0",
}


def setup_style():
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 11,
            "axes.titlesize": 14,
            "axes.labelsize": 11,
            "axes.edgecolor": COLORS["gray"],
            "axes.linewidth": 0.8,
            "axes.grid": True,
            "axes.axisbelow": True,
            "grid.color": "#DCE3E7",
            "grid.linewidth": 0.7,
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "savefig.facecolor": "white",
        }
    )


def save(fig, name):
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / name, dpi=240, bbox_inches="tight")
    plt.close(fig)


def figure_1_languages():
    fig = plt.figure(figsize=(12, 6.6))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.05, 1.55], wspace=0.28)
    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[0, 1])

    labels = ["Inglês", "Desconhecido", "Outros\nidentificados"]
    values = [89.70, 8.38, 1.92]
    colors = [COLORS["blue"], COLORS["gray"], COLORS["gold"]]
    bottom = 0
    for label, value, color in zip(labels, values, colors):
        ax1.bar(0, value, bottom=bottom, width=0.55, color=color, label=label)
        if value > 3:
            ax1.text(0, bottom + value / 2, f"{value:.2f}%".replace(".", ","),
                     ha="center", va="center", color="white", fontweight="bold")
        bottom += value
    ax1.set_ylim(0, 100)
    ax1.set_xlim(-0.6, 0.6)
    ax1.set_xticks([])
    ax1.set_ylabel("Participação no corpus (%)")
    ax1.set_title("Composição geral")
    ax1.legend(frameon=False, loc="lower center", bbox_to_anchor=(0.5, -0.21), ncol=1)
    ax1.grid(axis="x", visible=False)

    subset = DATA[(DATA.figura == 1) & DATA.grupo.isin(
        ["Alemão", "Francês", "Sueco", "Chinês", "Espanhol", "Russo", "Português"]
    )].copy()
    subset = subset.sort_values("valor", ascending=True)
    bar_colors = [COLORS["terracotta"] if x == "Português" else COLORS["teal"] for x in subset.grupo]
    bars = ax2.barh(subset.grupo, subset.valor, color=bar_colors, height=0.62)
    ax2.set_xlim(0, 0.205)
    ax2.set_xlabel("Participação no corpus (%)")
    ax2.set_title("Idiomas selecionados fora do inglês")
    for bar, value in zip(bars, subset.valor):
        ax2.text(value + 0.004, bar.get_y() + bar.get_height() / 2,
                 f"{value:.2f}%".replace(".", ","), va="center", color=COLORS["dark"])
    ax2.grid(axis="y", visible=False)

    fig.suptitle("O centro estatístico tem uma composição linguística", fontsize=18,
                 fontweight="bold", color=COLORS["dark"], y=1.02)
    fig.text(0.5, -0.03,
             "Fonte: Touvron et al. (2023), Llama 2, Tabela 10. Português = 0,09% de todo o corpus; não é uma medida específica de pt-BR.\n"
             "A distribuição de modelos proprietários recentes não é divulgada com esse grau de detalhe.",
             ha="center", va="top", fontsize=9, color="#53646D")
    save(fig, "figura-1-idiomas-llama2.png")


def figure_2_culture():
    df = DATA[DATA.figura == 2].copy()
    models = ["GPT-3", "GPT-3.5-turbo", "GPT-4", "GPT-4-turbo", "GPT-4o"]
    no_prompt = [float(df[(df.grupo == m) & df.metrica.str.contains("sem prompting")].valor.iloc[0]) for m in models]
    prompted = [float(df[(df.grupo == m) & df.metrica.str.contains("com prompting")].valor.iloc[0]) for m in models]

    x = np.arange(len(models))
    width = 0.36
    fig, ax = plt.subplots(figsize=(12, 6.5))
    b1 = ax.bar(x - width / 2, no_prompt, width, label="Resposta padrão", color=COLORS["terracotta"])
    b2 = ax.bar(x + width / 2, prompted, width, label="Identidade cultural no prompt", color=COLORS["teal"])
    ax.set_xticks(x, models)
    ax.set_ylabel("Distância cultural média (menor = melhor alinhamento)")
    ax.set_ylim(0, 3.8)
    ax.set_title("Prompts culturais reduzem a distância — mas não eliminam o desalinhamento",
                 fontsize=17, fontweight="bold", color=COLORS["dark"], pad=18)
    ax.legend(frameon=False, loc="upper left", ncol=2)
    ax.grid(axis="x", visible=False)
    for bars in (b1, b2):
        for bar in bars:
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.07,
                    f"{bar.get_height():.2f}".replace(".", ","), ha="center", va="bottom", fontsize=9)
    fig.text(0.5, -0.015,
             "Fonte: Tao et al. (2024), PNAS Nexus. Comparação com IVS/WVS em 107 países/territórios; respostas em inglês.\n"
             "O prompting melhorou o alinhamento em 71%–81% dos países para GPT-4/4-turbo/4o, mas piorou alguns casos.",
             ha="center", va="top", fontsize=9, color="#53646D")
    save(fig, "figura-2-alinhamento-cultural.png")


def figure_3_creativity():
    labels = ["Uma ideia\nde IA", "Até cinco ideias\nde IA"]
    novelty = [5.4, 8.1]
    similarity = [10.7, 8.9]
    fig, axes = plt.subplots(1, 2, figsize=(12, 6.4), gridspec_kw={"wspace": 0.28})

    bars1 = axes[0].bar(labels, novelty, color=COLORS["blue"], width=0.58)
    axes[0].set_ylim(0, 12)
    axes[0].set_ylabel("Ganho sobre o controle (%)")
    axes[0].set_title("Qualidade individual: novidade ↑", fontweight="bold")
    axes[0].grid(axis="x", visible=False)
    for bar, value in zip(bars1, novelty):
        axes[0].text(bar.get_x() + bar.get_width() / 2, value + 0.3,
                     f"+{value:.1f}%".replace(".", ","), ha="center", fontweight="bold")

    bars2 = axes[1].bar(labels, similarity, color=COLORS["terracotta"], width=0.58)
    axes[1].set_ylim(0, 14)
    axes[1].set_ylabel("Aumento de similaridade (% da amplitude do controle)")
    axes[1].set_title("Diversidade coletiva: similaridade ↑", fontweight="bold")
    axes[1].grid(axis="x", visible=False)
    for bar, value in zip(bars2, similarity):
        axes[1].text(bar.get_x() + bar.get_width() / 2, value + 0.35,
                     f"+{value:.1f}%".replace(".", ","), ha="center", fontweight="bold")

    fig.suptitle("O paradoxo central: melhores textos, textos mais parecidos",
                 fontsize=18, fontweight="bold", color=COLORS["dark"], y=1.02)
    fig.text(0.5, -0.02,
             "Fonte: Doshi & Hauser (2024), Science Advances. N = 293 escritores; 600 avaliadores; 3.519 avaliações.\n"
             "Os dois painéis usam métricas diferentes e não devem ser subtraídos entre si.",
             ha="center", va="top", fontsize=9, color="#53646D")
    save(fig, "figura-3-criatividade-diversidade.png")


def figure_4_learning():
    conditions = ["GPT Base", "GPT Tutor\n(com salvaguardas)"]
    practice = [48, 127]
    exam = [-17, 0]
    fig, axes = plt.subplots(1, 2, figsize=(12, 6.4), gridspec_kw={"wspace": 0.28})

    bars1 = axes[0].bar(conditions, practice, color=[COLORS["blue"], COLORS["teal"]], width=0.58)
    axes[0].set_ylim(0, 145)
    axes[0].set_ylabel("Diferença em relação ao controle (%)")
    axes[0].set_title("Durante a prática com IA", fontweight="bold")
    axes[0].grid(axis="x", visible=False)
    for bar, value in zip(bars1, practice):
        axes[0].text(bar.get_x() + bar.get_width() / 2, value + 4, f"+{value}%",
                     ha="center", fontweight="bold")

    bars2 = axes[1].bar(conditions, exam, color=[COLORS["terracotta"], COLORS["teal"]], width=0.58)
    axes[1].axhline(0, color=COLORS["dark"], linewidth=0.9)
    axes[1].set_ylim(-25, 12)
    axes[1].set_ylabel("Diferença em relação ao controle (%)")
    axes[1].set_title("Depois, em exame sem IA", fontweight="bold")
    axes[1].grid(axis="x", visible=False)
    axes[1].text(bars2[0].get_x() + bars2[0].get_width() / 2, -19.5, "−17%",
                 ha="center", va="top", fontweight="bold")
    axes[1].text(bars2[1].get_x() + bars2[1].get_width() / 2, 1.2, "≈ 0 (n.s.)",
                 ha="center", va="bottom", fontweight="bold")

    fig.suptitle("Desempenho imediato não é o mesmo que aprendizagem",
                 fontsize=18, fontweight="bold", color=COLORS["dark"], y=1.02)
    fig.text(0.5, -0.02,
             "Fonte: Bastani et al. (2025), PNAS. Experimento de campo com quase mil estudantes do ensino médio em matemática.\n"
             "O resultado sustenta uma implicação pedagógica; não mede criatividade ou identidade cultural.",
             ha="center", va="top", fontsize=9, color="#53646D")
    save(fig, "figura-4-aprendizagem-guardrails.png")


if __name__ == "__main__":
    setup_style()
    figure_1_languages()
    figure_2_culture()
    figure_3_creativity()
    figure_4_learning()
    print(f"Figuras gravadas em {OUT}")
