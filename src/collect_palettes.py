import requests
import json
import pandas as pd


URL = "https://colorhunt.co/php/feed.php"

data = {
    "step": 1,
    "sort": "popular",
    "tags": "",
    "timeframe": 4000
}

# Получаем данные от Color Hunt
response = requests.post(URL, data=data)

print("Status code:", response.status_code)

palettes = response.json()

print("Получено палитр:", len(palettes))

# Преобразуем данные
rows = []

for i, palette in enumerate(palettes, start=1):

    code = palette["code"]

    # Разделяем code на 4 цвета
    colors = [
        "#" + code[0:6],
        "#" + code[6:12],
        "#" + code[12:18],
        "#" + code[18:24]
    ]

    rows.append({
        "rank": i,
        "color_1": colors[0],
        "color_2": colors[1],
        "color_3": colors[2],
        "color_4": colors[3],
        "likes": int(palette["likes"]),
        "age": palette["date"]
    })

# Создаём DataFrame
df = pd.DataFrame(rows)

# Берём первые 100 самых популярных
df = df.head(100)

output_path = "data/palettes.csv"

df.to_csv(output_path, index=False)

print("\nДатасет сохранён:")
print(output_path)

print("\nПервые 5 палитр:")
print(df.head())

print("\nВсего палитр в датасете:", len(df))