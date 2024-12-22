import logging
from src.app.core.dataloader import DataLoader
from src.app.core.tokenizer import Tokenizer
from src.app.core.dataset import NicknamesDataset
from src.app.core.model import BertModel
from src.app.core.trainer import Trainer
from torch.utils.data import DataLoader as TorchDataLoader

import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))



logging.basicConfig(level=logging.INFO)

# Конфигурация гиперпараметров
config = {
    "batch_size": 8,
    "epochs": 5,
    "learning_rate": 5e-5
}

# 1. Загрузка и подготовка данных
logging.info("Загрузка данных...")
data_loader = DataLoader('src/data/dataset/processed_nicknames.json')
train_texts, test_texts, train_labels, test_labels = data_loader.prepare_data()
train_labels_encoded, test_labels_encoded, label_encoder = data_loader.encode_labels(train_labels, test_labels)

logging.info("Данные успешно загружены и подготовлены.")

# 2. Токенизация
logging.info("Запуск токенизации...")
tokenizer = Tokenizer()
train_encodings = tokenizer.tokenize(train_texts)
test_encodings = tokenizer.tokenize(test_texts)

logging.info("Токенизация завершена.")

# 3. Подготовка PyTorch датасетов
logging.info("Подготовка датасетов...")
train_dataset = NicknamesDataset(train_encodings, train_labels_encoded)
test_dataset = NicknamesDataset(test_encodings, test_labels_encoded)

train_loader = TorchDataLoader(train_dataset, batch_size=config["batch_size"], shuffle=True)
test_loader = TorchDataLoader(test_dataset, batch_size=config["batch_size"])

logging.info("Датасеты готовы.")

# 4. Инициализация модели
logging.info("Инициализация модели...")
model = BertModel(num_labels=len(label_encoder.classes_)).get_model()
logging.info("Модель успешно инициализирована.")

# 5. Обучение
logging.info("Запуск процесса обучения...")
trainer = Trainer(model, train_loader, test_loader, device='cpu')
trainer.train(epochs=config["epochs"])
logging.info("Обучение завершено.")

# 6. Оценка
logging.info("Оценка модели...")
evaluation_results = trainer.evaluate()
logging.info("Оценка завершена.")

# Вывод результатов
print(f"Accuracy: {evaluation_results['accuracy']}")
print(f"F1-Score: {evaluation_results['f1_score']}")

# Сохранение модели
logging.info("Сохранение модели...")
trainer.save_model('model_checkpoint.pth')
logging.info("Модель сохранена в model_checkpoint.pth.")

