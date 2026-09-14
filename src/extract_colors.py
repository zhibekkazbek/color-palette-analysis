from PIL import Image
from sklearn.cluster import KMeans
import numpy as np

IMAGE_PATH = "images/test_misa.jpeg"
image = Image.open(IMAGE_PATH)

# Переводим изображение в RGB
image = image.convert("RGB")

# Преобразуем изображение в массив пикселей
pixels = np.array(image)

# Превращаем матрицу изображения в список RGB-пикселей
pixels = pixels.reshape(-1, 3)

print("Количество пикселей:", len(pixels))

# K-means
kmeans = KMeans(
    n_clusters=4,
    random_state=42,
    n_init=10
)

kmeans.fit(pixels)

# Получаем центроиды кластеров
colors = kmeans.cluster_centers_

# Округляем RGB до целых чисел
colors = np.round(colors).astype(int)

print("\nДоминирующие цвета:")

for i, color in enumerate(colors, start=1):
    r, g, b = color

    print(
        f"Цвет {i}: "
        f"RGB({r}, {g}, {b})"
    )