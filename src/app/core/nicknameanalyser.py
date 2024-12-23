import json
from collections import Counter
import matplotlib.pyplot as plt


class NicknameAnalyzer:
    def __init__(self, json_path):
        self.json_path = json_path
        self.data = self.load_data()

    def load_data(self):
        try:
            with open(self.json_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            return data
        except Exception as e:
            print(f"Error loading JSON: {e}")
            return []

    def get_type_distribution(self):
        types = [entry['type'] for entry in self.data]
        return Counter(types)

    def get_gender_based_distribution(self):
        return {
            "male": Counter(entry['type'] for entry in self.data if entry['gender'] == 'male'),
            "female": Counter(entry['type'] for entry in self.data if entry['gender'] == 'female')
        }

    def get_education_based_distribution(self):
        education_types = ['humanitarian', 'technical', 'scientific']
        edu_distribution = {edu: Counter() for edu in education_types}

        for entry in self.data:
            edu = entry.get('education')
            if edu in edu_distribution:
                edu_distribution[edu][entry['type']] += 1

        return edu_distribution

    def visualize_type_distribution(self):
        type_counts = self.get_type_distribution()
        labels, counts = zip(*type_counts.items())

        # Настройка фигуры и шрифта
        plt.figure(figsize=(10, 6))
        plt.pie(
            counts, labels=labels, autopct='%1.1f%%', startangle=140,
            textprops={'fontsize': 12}
        )
        plt.title("Частотное распределение типов никнеймов", fontsize=16)
        plt.tight_layout()  # Улучшение компоновки
        plt.show()

    def visualize_gender_distribution(self):
        gender_counts = self.get_gender_based_distribution()

        # Настройка фигуры
        plt.figure(figsize=(10, 6))

        for gender, counts in gender_counts.items():
            labels, values = zip(*counts.items())
            plt.bar(labels, values, label=gender, alpha=0.7)

        plt.title("Типы никнеймов по полу", fontsize=16)
        plt.xlabel("Типы никнеймов", fontsize=12)
        plt.ylabel("Частота", fontsize=12)
        plt.xticks(rotation=45, fontsize=10)  # Поворот меток по оси X
        plt.yticks(fontsize=10)
        plt.legend(title="Пол", fontsize=12)
        plt.tight_layout()  # Улучшение компоновки
        plt.show()

    def visualize_education_distribution(self):
        edu_counts = self.get_education_based_distribution()

        # Настройка фигуры
        plt.figure(figsize=(12, 8))

        for edu, counts in edu_counts.items():
            labels, values = zip(*counts.items()) if counts else ([], [])
            plt.bar(labels, values, label=edu, alpha=0.7)

        plt.title("Типы никнеймов по образованию", fontsize=16)
        plt.xlabel("Типы никнеймов", fontsize=12)
        plt.ylabel("Частота", fontsize=12)
        plt.xticks(rotation=45, fontsize=10)  # Поворот меток по оси X
        plt.yticks(fontsize=10)
        plt.legend(title="Образование", fontsize=12)
        plt.tight_layout()  # Улучшение компоновки
        plt.show()


if __name__ == "__main__":

    # analyzer = NicknameAnalyzer('src/data/dataset/nicknames.json')
    analyzer = NicknameAnalyzer('src/data/dataset/processed_vkdata.json')

    print("Частотное распределение типов никнеймов:")
    print(analyzer.get_type_distribution())

    print("\nТипы никнеймов по полу:")
    print(analyzer.get_gender_based_distribution())

    print("\nТипы никнеймов по образованию:")
    print(analyzer.get_education_based_distribution())

    # Visualization examples
    analyzer.visualize_type_distribution()
    analyzer.visualize_gender_distribution()
    analyzer.visualize_education_distribution()
