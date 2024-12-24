# import json
#
# # Загрузка данных из трех файлов
# with open('src/data/dataset/user_names.json', 'r', encoding='utf-8') as f1, \
#         open('src/data/dataset/users.json', 'r', encoding='utf-8') as f2, \
#         open('src/data/dataset/classify_faculty.json', 'r', encoding='utf-8') as f3:
#     data1 = json.load(f1)  # Данные с screen_name
#     data2 = json.load(f2)  # Данные с sex
#     data3 = json.load(f3)  # Данные с education
#
# # Преобразуем данные из каждого файла в словари по id для удобства объединения
# data1_dict = {entry['id']: entry for entry in data1}
# data2_dict = {entry['id']: entry for entry in data2}
# data3_dict = {entry['id']: entry for entry in data3}
#
# # Функция для преобразования значения sex
# def transform_sex(sex_value):
#     if sex_value == 1:
#         return "female"
#     elif sex_value == 2:
#         return "male"
#     else:
#         return "undefined"
#
# # Объединяем данные, добавляем нужные поля с переименованием
# vkdata = []
# for id_, entry1 in data1_dict.items():
#     if id_ in data2_dict and id_ in data3_dict:
#         entry2 = data2_dict[id_]
#         entry3 = data3_dict[id_]
#
#         vkdata.append({
#             'nickname': entry1.get('screen_name', ''),
#             'gender': transform_sex(entry2.get('sex', 0)),
#             'education': entry3.get('education', ''),
#             'type': ""
#         })
#
# # Сохранение результата в новый JSON файл
# output_file_path = 'src/data/dataset/vkdata.json'
# with open(output_file_path, 'w', encoding='utf-8') as f_out:
#     json.dump(vkdata, f_out, ensure_ascii=False, indent=4)
#
# print(f"Объединённые данные сохранены в {output_file_path}")

import json

# Загрузка данных из трех файлов
with open('src/data/dataset/user_names.json', 'r', encoding='utf-8') as f1, \
        open('src/data/dataset/users.json', 'r', encoding='utf-8') as f2, \
        open('src/data/dataset/classify_faculty.json', 'r', encoding='utf-8') as f3:
    data1 = json.load(f1)  # Данные с screen_name
    data2 = json.load(f2)  # Данные с sex
    data3 = json.load(f3)  # Данные с education

# Преобразуем данные из каждого файла в словари по id для удобства объединения
data1_dict = {entry['id']: entry for entry in data1}
data2_dict = {entry['id']: entry for entry in data2}
data3_dict = {entry['id']: entry for entry in data3}

# Функция для преобразования значения sex
def transform_sex(sex_value):
    if sex_value == 1:
        return "female"
    elif sex_value == 2:
        return "male"
    else:
        return "undefined"

# Объединяем данные, добавляем нужные поля с переименованием
vkdata = []
for id_, entry1 in data1_dict.items():
    if id_ in data2_dict and id_ in data3_dict:
        entry2 = data2_dict[id_]
        entry3 = data3_dict[id_]

        nickname = entry1.get('screen_name', '')
        gender = transform_sex(entry2.get('sex', 0))
        education = entry3.get('education', '')

        # Условие для фильтрации записей
        if gender != "undefined" and education != "" and nickname not in ("", None):
            vkdata.append({
                'nickname': nickname,
                'gender': gender,
                'education': education,
                'type': ""
            })

# Сохранение результата в новый JSON файл
output_file_path = 'src/data/dataset/vkdata.json'
with open(output_file_path, 'w', encoding='utf-8') as f_out:
    json.dump(vkdata, f_out, ensure_ascii=False, indent=4)

print(f"Объединённые данные сохранены в {output_file_path}")
