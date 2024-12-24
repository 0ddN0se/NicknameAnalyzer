import json
import matplotlib.pyplot as plt
import pandas as pd


class ExperimentAnalyzer:
    def __init__(self, json_path):
        """
        Инициализация класса с указанием пути к JSON файлу.
        """
        self.json_path = json_path
        self.data = self.load_data()

    def load_data(self):
        """
        Загрузка данных из JSON файла.
        """
        try:
            with open(self.json_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            return data
        except Exception as e:
            print(f"Error loading JSON: {e}")
            return []

    def plot_accuracy(self):
        """
        Построение графика Accuracy vs Epochs.
        """
        self._plot_metric("accuracy", "Accuracy")

    def plot_precision(self):
        """
        Построение графика Precision vs Epochs.
        """
        self._plot_metric("precision", "Precision")

    def plot_recall(self):
        """
        Построение графика Recall vs Epochs.
        """
        self._plot_metric("recall", "Recall")

    def plot_f1_score(self):
        """
        Построение графика F1-Score vs Epochs.
        """
        self._plot_metric("f1_score", "F1-Score")

    def plot_auc_roc(self):
        """
        Построение графика AUC-ROC vs Epochs.
        """
        self._plot_metric("auc_roc", "AUC-ROC")

    def _plot_metric(self, metric_key, metric_name):
        """
        Внутренний метод для построения графиков.
        """
        if not self.data:
            print("Данные не загружены. Проверьте JSON файл.")
            return

        values = [entry["metrics"][metric_key] for entry in self.data]
        epochs = [entry["config"]["epochs"] for entry in self.data]
        batch_sizes = [entry["config"]["batch_size"] for entry in self.data]

        plt.figure(figsize=(10, 6))
        plt.scatter(epochs, values, c=batch_sizes, cmap='viridis', s=100, alpha=0.7, label="Batch Size")
        plt.colorbar(label="Batch Size")
        plt.plot(epochs, values, linestyle='--', alpha=0.5)
        plt.title(f"{metric_name} vs Epochs")
        plt.xlabel("Epochs")
        plt.ylabel(metric_name)
        plt.grid(True, linestyle="--", alpha=0.6)
        plt.legend(loc="best")
        plt.show()

    def export_to_excel(self, excel_path):
        """
        Экспорт данных в Excel файл.
        """
        if not self.data:
            print("Данные не загружены. Проверьте JSON файл.")
            return

        rows = []
        for entry in self.data:
            row = {
                "id": entry["id"],
                "batch_size": entry["config"]["batch_size"],
                "epochs": entry["config"]["epochs"],
                "accuracy": entry["metrics"]["accuracy"],
                "precision": entry["metrics"]["precision"],
                "recall": entry["metrics"]["recall"],
                "f1_score": entry["metrics"]["f1_score"],
                "auc_roc": entry["metrics"]["auc_roc"],
                "losses": entry["losses"],
            }
            rows.append(row)

        df = pd.DataFrame(rows)
        df.to_excel(excel_path, index=False)
        print(f"Данные успешно записаны в {excel_path}")
