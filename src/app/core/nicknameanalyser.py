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

        total = sum(counts)
        percentages = [count / total * 100 for count in counts]

        plt.figure(figsize=(12, 6))
        bars = plt.bar(labels, counts, color='skyblue', alpha=0.7)

        for bar, percentage in zip(bars, percentages):
            plt.text(
                bar.get_x() + bar.get_width() / 2, bar.get_height(),
                f'{percentage:.1f}%', ha='center', va='bottom', fontsize=10
            )

        plt.title("Частотное распределение типов никнеймов", fontsize=16)
        plt.xlabel("Типы никнеймов", fontsize=12)
        plt.ylabel("Частота", fontsize=12)
        plt.xticks(rotation=45, fontsize=10)
        plt.tight_layout()
        plt.show()

    def visualize_gender_distribution(self):
        gender_counts = self.get_gender_based_distribution()

        plt.figure(figsize=(12, 6))

        total_counts = {gender: sum(counts.values()) for gender, counts in gender_counts.items()}

        for gender, counts in gender_counts.items():
            labels, values = zip(*counts.items())
            total = total_counts[gender]
            percentages = [value / total * 100 for value in values]

            bars = plt.bar(labels, values, label=gender, alpha=0.7)

            for bar, percentage in zip(bars, percentages):
                plt.text(
                    bar.get_x() + bar.get_width() / 2, bar.get_height(),
                    f'{percentage:.1f}%', ha='center', va='bottom', fontsize=10
                )

        plt.title("Типы никнеймов по полу", fontsize=16)
        plt.xlabel("Типы никнеймов", fontsize=12)
        plt.ylabel("Частота", fontsize=12)
        plt.xticks(rotation=45, fontsize=10)
        plt.legend(title="Пол", fontsize=12)
        plt.tight_layout()
        plt.show()

    def visualize_education_distribution(self):
        edu_counts = self.get_education_based_distribution()

        plt.figure(figsize=(12, 6))

        total_counts = {edu: sum(counts.values()) for edu, counts in edu_counts.items() if counts}

        for edu, counts in edu_counts.items():
            if not counts:
                continue
            labels, values = zip(*counts.items())
            total = total_counts[edu]
            percentages = [value / total * 100 for value in values]

            bars = plt.bar(labels, values, label=edu, alpha=0.7)

            for bar, percentage in zip(bars, percentages):
                plt.text(
                    bar.get_x() + bar.get_width() / 2, bar.get_height(),
                    f'{percentage:.1f}%', ha='center', va='bottom', fontsize=10
                )

        plt.title("Типы никнеймов по образованию", fontsize=16)
        plt.xlabel("Типы никнеймов", fontsize=12)
        plt.ylabel("Частота", fontsize=12)
        plt.xticks(rotation=45, fontsize=10)
        plt.legend(title="Образование", fontsize=12)
        plt.tight_layout()
        plt.show()
