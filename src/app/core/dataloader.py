import json
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder


class DataLoader:
    def __init__(self, json_path):
        self.json_path = json_path

    def load_data(self):
        with open(self.json_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        # Используем текстовые токены из processed для текста
        texts = [" ".join(token["lemma"] for token in entry["processed"]) for entry in data]
        # Используем поле type как целевую переменную
        labels = [entry["type"] for entry in data]
        return texts, labels

    def prepare_data(self, test_size=0.2):
        texts, labels = self.load_data()
        train_texts, test_texts, train_labels, test_labels = train_test_split(
            texts, labels, test_size=test_size, random_state=42
        )
        return train_texts, test_texts, train_labels, test_labels

    def encode_labels(self, train_labels, test_labels):
        label_encoder = LabelEncoder()
        train_labels_encoded = label_encoder.fit_transform(train_labels)
        test_labels_encoded = label_encoder.transform(test_labels)
        return train_labels_encoded, test_labels_encoded, label_encoder
