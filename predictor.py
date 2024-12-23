import torch
from src.app.core.tokenizer import Tokenizer
from src.app.core.model import BertModel
from torch.utils.data import DataLoader
from sklearn.preprocessing import LabelEncoder

# Загрузка модели и токенизатора
def load_model(model_path='model_checkpoint.pth'):
    # Загрузка модели
    model = BertModel(num_labels=3).get_model()  # предполагаем, что у нас 3 класса
    model.load_state_dict(torch.load(model_path))
    model.eval()
    return model

# Функция для предсказания
def predict_nickname(nickname, model, tokenizer, label_encoder):
    encoding = tokenizer.tokenize([nickname])
    inputs = {key: torch.tensor(val) for key, val in encoding.items()}
    with torch.no_grad():
        outputs = model(**inputs)
        preds = torch.argmax(outputs.logits, axis=1)
        predicted_label = label_encoder.inverse_transform(preds.cpu().numpy())[0]
    return predicted_label

# Пример использования
if __name__ == "__main__":
    # Загружаем модель и токенизатор
    model = load_model('model_checkpoint_vk.pth')
    tokenizer = Tokenizer()
    label_encoder = LabelEncoder()
    label_encoder.fit(['неопределенный', 'номинативный', 'составной'])  # Обучаем на возможных метках

    # Ввод никнейма
    nickname = input("Введите никнейм: ")
    predicted_label = predict_nickname(nickname, model, tokenizer, label_encoder)

    print(f"Предсказанный признак для никнейма '{nickname}': {predicted_label}")
