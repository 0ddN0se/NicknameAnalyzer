import json

# Функция для классификации факультетов
def classify_faculty(faculty_name):
    if any(word in faculty_name.lower() for word in ["эконом", "юрид", "лингвист", "истор", "медиа", "культур", "искусств", "перевод", "филолог", "международ", "прав", "розыск","юрис",  "адвокат", "дизайн", "творч", "финанс", "коммер", "админ", "теолог", "юстиц", "polit", "налог", "туризм", "изкуств", "менеджмент", "admin", "банк", "сервис","маркет", "полит", "turism", "журнал", "литера", "гуманитар", "business", "иностр", "исполнит", "бизнес", "музык", "business", "бухгалтер", "предпринимат", "социал", "уманит", "торгов", "воен", "детектив"]):
        return "humanitarian"
    if any(word in faculty_name for word in ["Ekonom", "Human", "Language", "Administr", "Communication", "Сервис", "Журналист", "Театр", "Бизнес", "Гуманитар", "Theology", "Финанс", "Manag", "Туризм", "Econom", "Регион", "Хор", "Sociolog", "Market", "Социолог", "Philosophy",  "Режис", "Следств",  "Живопис", "Документ","Design", "Turizm","English", "Social", "Music", "Textile", "Filolog", "Істор", "Менеджмент", "Коммерция", "Dram", "Vocal", "MBA", "Media", "Lingue", "Восточ", "Turism", "Business", "Исполнит", "Музык", "Бухгалтер", "Предпринимат", "Социал", "Хуманит", "Finance", "Dance", "Актер", "Art", "Регент", "Law", "Учет", "Commerce", "Tourism"]):
        return "humanitarian"
    elif any(word in faculty_name.lower() for word in ["инженер", "строит", "механ", "техн", "кибер", "програм", "транспорт", "строен", "Энерг", "электр", "прибор", "радиотех", "информ", "вожден", "авиац", "производ", "слесар", "автомат", "інформац", "математ", "arquitetura", "texnol", "ingen", "matemat", "конструктор", "informat", "телекоммуникац"]):
        return "technical"
    elif any(word in faculty_name for word in ["Энергет", "Радиотех", "Teknik", "Engine", "Автомат", "Математ", "Arquitetura", "Ingen", "Архитектур", "Tecnolog", "Конструктор", "Авто", "Металлург", "Matem", "Engen","Físic", "Technolog", "Inform", "Game", "Дорожн", "Sistem", "энергетич", "inform" "Машиностроит", "Arhitekt", "Computer","Графики", "Тепло","качеств", "Astronom", "Bildung", "Компьютер", "Gráfic", "Ingin", "Mecan", "Gradit", "Architect"]):
        return "technical"
    elif any(word in faculty_name.lower() for word in ["биолог", "медицин", "психолог", "геолог", "физ", "хим", "эколог", "географ", "спорт", "science", "здоров", "образован", "криминал", "научн", "нефт", "естеств",  "лечебн", "педагог", "здравоохран","хоз", "садовод", "bio", "fiz", "безопасност", "защит", "сестр"]):
        return "scientific"
    elif any(word in faculty_name for word in ["Medic", "Стоматолог", "Educat", "Педиатр", "Фармац", "Агро", "Лечебн", "Педагог", "Bio", "Мед", "Гор", "Médecin", "Почв", "Гидролог", "Pharmacy", "ВДВ", "Развед", "Odontol", "Agronom", "Psikolog", "Плод", "Ветеринар", "Dentist", "Agric", "Stomatol", "Фарма", "Сад", 'природ', "оруж", "Офицер", "Psycholog"]):
        return "scientific"
    else:
        return ""

# Считываем JSON-файл
input_file_path = "src/data/dataset/faculty_data_filtered.json"  # Замените на путь к вашему входному файлу
output_file_path = "src/data/dataset/classify_faculty.json"  # Путь для сохранения результата

with open(input_file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Добавляем поле education
for entry in data:
    if "faculty_name" in entry:
        entry["education"] = classify_faculty(entry["faculty_name"])

# Сохраняем результат в новый файл
with open(output_file_path, 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

print(f"Обновлённые данные сохранены в {output_file_path}")
