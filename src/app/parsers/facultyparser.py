# import json
#
# # Загрузка данных из второго JSON-файла
# with open('src/data/dataset/users.json', 'r', encoding='utf-8') as f:
#     data = json.load(f)
#
# # Извлечение уникальных faculty
# unique_faculties = set()
# for entry in data:
#     faculty = entry.get('faculty')
#     if faculty not in (0, None):  # Исключаем, если faculty равен 0 или None
#         unique_faculties.add(faculty)
#
# # Сохранение уникальных значений в файл
# with open('unique_faculties.json', 'w', encoding='utf-8') as f_out:
#     json.dump(list(unique_faculties), f_out, ensure_ascii=False, indent=4)
#
# print("Уникальные faculty успешно сохранены в 'unique_faculties.json'")

import json

# Загрузка данных из второго JSON-файла
with open('src/data/dataset/users.json', 'r', encoding='utf-8') as f:
    data2 = json.load(f)

# Извлечение записей с валидным faculty
faculty_data = []
for entry in data2:
    faculty = entry.get('faculty')
    if faculty not in (0, None):  # Исключаем, если faculty равен 0 или None
        faculty_data.append({
            'id': entry['id'],
            'faculty': faculty,
            'faculty_name': entry.get('faculty_name', None)
        })

# Сохранение результата в новый JSON
with open('src/data/dataset/faculty_data_filtered.json', 'w', encoding='utf-8') as f_out:
    json.dump(faculty_data, f_out, ensure_ascii=False, indent=4)

print("Фильтрованные данные о факультетах успешно сохранены в 'faculty_data_filtered.json'")

