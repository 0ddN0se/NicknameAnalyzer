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
        plt.pie(counts, labels=labels, autopct='%1.1f%%', startangle=140)
        plt.title("Частотное распределение типов никнеймов")
        plt.show()

    def visualize_gender_distribution(self):

        gender_counts = self.get_gender_based_distribution()
        for gender, counts in gender_counts.items():
            labels, values = zip(*counts.items())
            plt.bar(labels, values, label=gender)

        plt.title("Типы никнеймов по полу")
        plt.xlabel("Типы никнеймов")
        plt.ylabel("Частота")
        plt.legend()
        plt.show()

    def visualize_education_distribution(self):

        edu_counts = self.get_education_based_distribution()


        for edu in edu_counts:
            labels, values = zip(*edu_counts[edu].items()) if edu_counts[edu] else ([], [])
            plt.bar(labels, values, label=edu)

        plt.title("Типы никнеймов по образованию")
        plt.xlabel("Типы никнеймов")
        plt.ylabel("Частота")
        plt.legend()
        plt.show()

if __name__ == "__main__":

    analyzer = NicknameAnalyzer('src/data/dataset/nicknames.json')

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
