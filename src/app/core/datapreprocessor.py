import json
from src.app.core.nickspreparator import NicknameProcessor


class DataPreprocessor:
    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path
        self.processor = NicknameProcessor()

    def load_data(self):
        """Загрузка исходного JSON-файла с никнеймами."""
        with open(self.input_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    def save_data(self, data):
        """Сохранение обработанных данных в JSON-файл."""
        with open(self.output_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def preprocess_data(self):
        """Основной метод для предобработки данных."""
        raw_data = self.load_data()
        processed_data = []

        for entry in raw_data:
            nickname = entry['nickname']

            # Получение частей речи, лемм и стеммов
            processed_parts = self.processor.analyze(nickname)

            # Если type не указан, определяем его
            word_type = entry.get("type", "").strip()
            if not word_type:
                word_type = self.processor.classify_type(nickname)

            # Формируем структуру с предобработкой
            processed_data.append({
                "nickname": nickname,
                "gender": entry.get("gender", ""),
                "education": entry.get("education", ""),
                "type": word_type,  # Учитываем существующее значение или генерируем новое
                "processed": processed_parts
            })

        self.save_data(processed_data)


