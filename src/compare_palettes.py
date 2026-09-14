import math
from itertools import permutations

import pandas as pd
import os

DATASET_PATH = "data/palettes.csv"
OUTPUT_PATH = "results/similar_palettes.csv"

IMAGE_PALETTE = [
    "#A28465",
    "#271E19",
    "#F9ECE0",
    "#C0BA88"
]

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")

    return (
        int(hex_color[0:2], 16),
        int(hex_color[2:4], 16),
        int(hex_color[4:6], 16)
    )

def rgb_distance(color1, color2):
    r1, g1, b1 = color1
    r2, g2, b2 = color2

    distance = math.sqrt(
        (r1 - r2) ** 2 +
        (g1 - g2) ** 2 +
        (b1 - b2) ** 2
    )

    # Нормализация расстояния к диапазону [0, 1]
    max_distance = math.sqrt(3 * 255 ** 2)

    return distance / max_distance

def fuzzy_similarity(distance, sigma=0.25):
    """
    Гауссовской функции принадлежности.
    distance = 0 → similarity = 1
    Чем больше distance, тем меньше similarity.
    """

    return math.exp(
        -(distance ** 2) / (2 * sigma ** 2)
    )

def palette_similarity(image_palette, colorhunt_palette):

    image_rgb = [
        hex_to_rgb(color)
        for color in image_palette
    ]

    colorhunt_rgb = [
        hex_to_rgb(color)
        for color in colorhunt_palette
    ]

    best_similarity = -1
    best_permutation = None

    # 4! = 24 (перебор всех возможных соответствий)
    for permutation in permutations(range(4)):

        total_similarity = 0

        for i in range(4):

            image_color = image_rgb[i]

            colorhunt_color = colorhunt_rgb[
                permutation[i]
            ]

            distance = rgb_distance(
                image_color,
                colorhunt_color
            )

            similarity = fuzzy_similarity(distance)

            total_similarity += similarity

        average_similarity = total_similarity / 4

        if average_similarity > best_similarity:
            best_similarity = average_similarity
            best_permutation = permutation

    return best_similarity, best_permutation

# Загрузка датасета
df = pd.read_csv(DATASET_PATH)

print("Загружено палитр:", len(df))
print()

# Сравнение с каждой палитрой
results = []

for _, row in df.iterrows():

    colorhunt_palette = [
        row["color_1"],
        row["color_2"],
        row["color_3"],
        row["color_4"]
    ]

    similarity, permutation = palette_similarity(
        IMAGE_PALETTE,
        colorhunt_palette
    )

    results.append({
        "palette_rank": row["rank"],
        "color_1": row["color_1"],
        "color_2": row["color_2"],
        "color_3": row["color_3"],
        "color_4": row["color_4"],
        "likes": row["likes"],
        "age": row["age"],
        "similarity": similarity
    })

# Сортировка
results_df = pd.DataFrame(results)

results_df = results_df.sort_values(
    by="similarity",
    ascending=False
).reset_index(drop=True)

results_df.insert(
    0,
    "similarity_rank",
    range(1, len(results_df) + 1)
)

os.makedirs("results", exist_ok=True)

# Сохранение результата
results_df.to_csv(
    OUTPUT_PATH,
    index=False
)

# Вывод Топ-10
print("========================================")
print("TOP-10 наиболее похожих палитр")
print("========================================\n")

top_10 = results_df.head(10)

for _, row in top_10.iterrows():

    colors = (
        f"{row['color_1']} "
        f"{row['color_2']} "
        f"{row['color_3']} "
        f"{row['color_4']}"
    )

    print(
        f"{int(row['similarity_rank']):2d}. "
        f"{colors} | "
        f"Similarity: {row['similarity']:.4f} "
        f"({row['similarity'] * 100:.2f}%)"
    )


print("\n========================================")
print("Результаты сохранены:")
print(OUTPUT_PATH)
print("========================================")