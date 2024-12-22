import torch
from transformers import AdamW
from sklearn.metrics import classification_report

class Trainer:
    def __init__(self, model, train_loader, test_loader, device='cpu'):
        self.model = model.to(device)
        self.train_loader = train_loader
        self.test_loader = test_loader
        self.device = device
        self.optimizer = AdamW(self.model.parameters(), lr=5e-5)

    def train(self, epochs):
        self.model.train()
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
            print(f"Epoch {epoch + 1}, Loss: {total_loss / len(self.train_loader)}")

    def evaluate(self):
        self.model.eval()
        predictions, true_labels = [], []
        with torch.no_grad():
            for batch in self.test_loader:
                inputs, labels = batch
                inputs = {key: val.to(self.device) for key, val in inputs.items()}
                labels = labels.to(self.device)
                outputs = self.model(**inputs)
                preds = torch.argmax(outputs.logits, axis=1)
                predictions.extend(preds.tolist())
                true_labels.extend(labels.tolist())
        report = classification_report(true_labels, predictions, output_dict=True)
        return {"accuracy": report["accuracy"], "f1_score": report["macro avg"]["f1-score"]}

    def save_model(self, path):
        torch.save(self.model.state_dict(), path)


