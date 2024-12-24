import torch
import numpy as np
from sklearn.preprocessing import label_binarize
from transformers import AdamW
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score


class Trainer:
    def __init__(self, model, train_loader, test_loader, device='cpu'):
        self.model = model.to(device)
        self.train_loader = train_loader
        self.test_loader = test_loader
        self.device = device
        self.optimizer = AdamW(self.model.parameters(), lr=5e-5)

    def train(self, epochs):
        self.model.train()
        epoch_losses = []  # Список для записи потерь
        for epoch in range(epochs):
            total_loss = 0
            for batch in self.train_loader:
                inputs, labels = batch
                inputs = {key: val.to(self.device) for key, val in inputs.items()}
                labels = labels.to(self.device)
                outputs = self.model(**inputs, labels=labels)
                loss = outputs.loss
                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()
                total_loss += loss.item()
            avg_loss = total_loss / len(self.train_loader)
            epoch_losses.append(avg_loss)  # Сохраняем среднюю потерю за эпоху
            print(f"Epoch {epoch + 1}, Loss: {avg_loss}")
        return epoch_losses  # Возвращаем список потерь

    def evaluate(self):
        self.model.eval()
        predictions, true_labels, probabilities = [], [], []
        with torch.no_grad():
            for batch in self.test_loader:
                inputs, labels = batch
                inputs = {key: val.to(self.device) for key, val in inputs.items()}
                labels = labels.to(self.device)
                outputs = self.model(**inputs)

                # Вероятности (softmax для многоклассовой классификации)
                probs = torch.nn.functional.softmax(outputs.logits, dim=1)
                preds = torch.argmax(probs, axis=1)

                predictions.extend(preds.tolist())
                true_labels.extend(labels.tolist())
                probabilities.extend(probs.cpu().numpy())  # Для AUC-ROC

        # Преобразование вероятностей в NumPy-массив
        probabilities = np.array(probabilities)

        # Убедимся, что число классов совпадает
        all_classes = list(range(probabilities.shape[1]))
        true_labels_binarized = label_binarize(true_labels, classes=all_classes)

        # Расчёт метрик
        accuracy = accuracy_score(true_labels, predictions)
        precision = precision_score(true_labels, predictions, average="macro")
        recall = recall_score(true_labels, predictions, average="macro")
        f1 = f1_score(true_labels, predictions, average="macro")
        # auc_roc = roc_auc_score(true_labels_binarized, probabilities, multi_class="ovo")
        auc_roc = roc_auc_score(true_labels_binarized, probabilities, average="weighted", multi_class="ovo")

        # Возвращаем метрики
        return {
            "accuracy": accuracy,
            "precision": precision,
            "recall": recall,
            "f1_score": f1,
            "auc_roc": auc_roc
        }

    def save_model(self, path):
        torch.save(self.model.state_dict(), path)


