import json
import re  # Для проверки паттерна "id" с цифрами

# Функция для определения типа
def determine_type(nickname):
    if re.match(r'^id\d+$', nickname):  # Если nickname соответствует паттерну "id" + цифры
        return "неопределенный"
    else:
        return ""

# Загрузка данных из JSON-файла
input_file = "src/data/dataset/vkdata.json"  # Замените на путь к вашему JSON-файлу
output_file = "src/data/dataset/vkdata.json"  # Путь для сохранения результата

with open(input_file, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Обновление поля type
for entry in data:
    if "nickname" in entry:
        entry["type"] = determine_type(entry["nickname"])

# Сохранение обновлённого JSON
with open(output_file, 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

print(f"Обновлённые данные сохранены в {output_file}")
