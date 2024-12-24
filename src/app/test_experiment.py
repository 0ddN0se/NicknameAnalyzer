import pytest
import json
import os
from core.dataloader import DataLoader
from core.tokenizer import Tokenizer
from core.dataset import NicknamesDataset
from core.model import BertModel
from core.trainer import Trainer
from torch.utils.data import DataLoader as TorchDataLoader


@pytest.mark.parametrize(
    "batch_size, epochs, data_link",
    [
        (8, 1, "src/data/dataset/processed_nicknames.json"),
        (8, 2, "src/data/dataset/processed_nicknames.json"),
        (8, 3, "src/data/dataset/processed_nicknames.json"),
        (8, 4, "src/data/dataset/processed_nicknames.json"),
        (8, 5, "src/data/dataset/processed_nicknames.json"),
        (8, 6, "src/data/dataset/processed_nicknames.json"),
        (8, 7, "src/data/dataset/processed_nicknames.json"),
        (8, 8, "src/data/dataset/processed_nicknames.json"),
        (8, 9, "src/data/dataset/processed_nicknames.json"),
        (8, 10, "src/data/dataset/processed_nicknames.json"),
        (16, 1, "src/data/dataset/processed_nicknames.json"),
        (16, 2, "src/data/dataset/processed_nicknames.json"),
        (16, 3, "src/data/dataset/processed_nicknames.json"),
        (16, 4, "src/data/dataset/processed_nicknames.json"),
        (16, 5, "src/data/dataset/processed_nicknames.json"),
        (16, 6, "src/data/dataset/processed_nicknames.json"),
        (16, 7, "src/data/dataset/processed_nicknames.json"),
        (16, 8, "src/data/dataset/processed_nicknames.json"),
        (16, 9, "src/data/dataset/processed_nicknames.json"),
        (16, 10, "src/data/dataset/processed_nicknames.json"),
        (32, 1, "src/data/dataset/processed_nicknames.json"),
        (32, 2, "src/data/dataset/processed_nicknames.json"),
        (32, 3, "src/data/dataset/processed_nicknames.json"),
        (32, 4, "src/data/dataset/processed_nicknames.json"),
        (32, 5, "src/data/dataset/processed_nicknames.json"),
        (32, 6, "src/data/dataset/processed_nicknames.json"),
        (32, 7, "src/data/dataset/processed_nicknames.json"),
        (32, 8, "src/data/dataset/processed_nicknames.json"),
        (32, 9, "src/data/dataset/processed_nicknames.json"),
        (32, 10, "src/data/dataset/processed_nicknames.json"),

        # (8, 4, "src/data/dataset/processed_vkdata.json"),
        # (8, 6, "src/data/dataset/processed_vkdata.json"),
        # (8, 8, "src/data/dataset/processed_vkdata.json"),
        # (8, 10, "src/data/dataset/processed_vkdata.json"),
        # (16, 4, "src/data/dataset/processed_vkdata.json"),
        # (16, 6, "src/data/dataset/processed_vkdata.json"),
        # (16, 8, "src/data/dataset/processed_vkdata.json"),
        # (16, 10, "src/data/dataset/processed_vkdata.json"),
        # (32, 4, "src/data/dataset/processed_vkdata.json"),
        # (32, 6, "src/data/dataset/processed_vkdata.json"),
        # (32, 8, "src/data/dataset/processed_vkdata.json"),
        # (32, 10, "src/data/dataset/processed_vkdata.json"),
        # (32, 1, "src/data/dataset/processed_nicknames.json"),
        # (32, 1, "src/data/dataset/processed_vkdata.json"),
    ]
)
def test_experiment(batch_size, epochs, data_link):
    """
    Тест-эксперимент для обучения модели с разными параметрами.
    """
    # Конфигурация гиперпараметров
    config = {
        "batch_size": batch_size,
        "epochs": epochs,
        "learning_rate": 5e-5
    }

    # Лог для эксперимента
    experiment_log = {
        "id": f"{batch_size}_{epochs}_{data_link}",
        "config": config,
        "metrics": {},
        "losses": ""
    }

    # 1. Загрузка и подготовка данных
    data_loader = DataLoader(data_link)
    train_texts, test_texts, train_labels, test_labels = data_loader.prepare_data()
    train_labels_encoded, test_labels_encoded, label_encoder = data_loader.encode_labels(train_labels, test_labels)

    # 2. Токенизация
    tokenizer = Tokenizer()
    train_encodings = tokenizer.tokenize(train_texts)
    test_encodings = tokenizer.tokenize(test_texts)

    # 3. Подготовка PyTorch датасетов
    train_dataset = NicknamesDataset(train_encodings, train_labels_encoded)
    test_dataset = NicknamesDataset(test_encodings, test_labels_encoded)

    train_loader = TorchDataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    test_loader = TorchDataLoader(test_dataset, batch_size=batch_size)

    # 4. Инициализация модели
    model = BertModel(num_labels=len(label_encoder.classes_)).get_model()

    # 5. Обучение
    trainer = Trainer(model, train_loader, test_loader, device='cpu')
    losses = trainer.train(epochs=config["epochs"])  # Получаем потери по эпохам
    # Преобразуем список потерь в строку
    experiment_log["losses"] = " | ".join([f"Epoch {i + 1}: Loss {loss:.4f}" for i, loss in enumerate(losses)])

    # 6. Оценка
    evaluation_results = trainer.evaluate()
    experiment_log["metrics"] = evaluation_results

    output_path = "src/data/experiments/experiment_results.json"
    try:
        with open(output_path, 'r', encoding='utf-8') as log_file:
            all_results = json.load(log_file)
    except FileNotFoundError:
        all_results = []

    all_results.append(experiment_log)

    with open(output_path, 'w', encoding='utf-8') as log_file:
        json.dump(all_results, log_file, ensure_ascii=False, indent=4)

    # Убедимся, что метрики вычислены корректно
    assert evaluation_results["accuracy"] > 0, "Accuracy должна быть больше 0"
    assert evaluation_results["f1_score"] > 0, "F1-Score должна быть больше 0"

