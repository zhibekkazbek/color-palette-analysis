import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

RESULTS_PATH = "results/similar_palettes.csv"

df = pd.read_csv(RESULTS_PATH)
top_10 = df.head(10)

# Создаём график для Топ-10 для корректной визуализации
fig, ax = plt.subplots(figsize=(12, 10))

for row_index, (_, row) in enumerate(top_10.iterrows()):

    colors = [
        row["color_1"],
        row["color_2"],
        row["color_3"],
        row["color_4"]
    ]

    similarity = row["similarity"] * 100

    # Название палитры
    ax.text(
        -0.02,
        row_index + 0.5,
        f"#{row_index + 1}",
        ha="right",
        va="center",
        fontsize=12,
        fontweight="bold"
    )

    # Рисуем четыре цвета
    for color_index, color in enumerate(colors):

        rectangle = Rectangle(
            (color_index, row_index),
            1,
            1,
            facecolor=color
        )

        ax.add_patch(rectangle)

    # Similarity 
    ax.text(
        4.15,
        row_index + 0.5,
        f"{similarity:.2f}%",
        va="center",
        fontsize=11
    )

# Исходная палитра
input_y = 10.5

ax.text(
    -0.02,
    input_y + 0.5,
    "INPUT",
    ha="right",
    va="center",
    fontsize=12,
    fontweight="bold"
)

for color_index, color in enumerate([
    "#A28465",
    "#271E19",
    "#F9ECE0",
    "#C0BA88"
]):

    rectangle = Rectangle(
        (color_index, input_y),
        1,
        1,
        facecolor=color
    )

    ax.add_patch(rectangle)

ax.text(
    4.15,
    input_y + 0.5,
    "Image palette",
    va="center",
    fontsize=11,
    fontweight="bold"
)

ax.set_xlim(-0.8, 5.2)
ax.set_ylim(0, 12)

ax.set_aspect("equal")

ax.axis("off")

plt.title(
    "Top-10 Color Hunt palettes similar to the input image",
    fontsize=15,
    pad=20
)

plt.tight_layout()

plt.savefig(
    "results/top10_palettes.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()