import re
import spacy
from nltk.stem import SnowballStemmer


class NicknameProcessor:
    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')
        self.stemmer = SnowballStemmer(language='english')

    def preprocess_nickname(self, nickname):
        """
        Предварительная обработка никнейма: разбиение на части.
        """
        # Разбиваем на части по подчеркиваниям, пробелам и границам между буквами и цифрами
        parts = re.findall(r'[A-Za-z]+|\d+|_', nickname)
        return [part for part in parts if part.strip()]

    def analyze(self, nickname):
        """
        Анализ одного никнейма: лемматизация, стемминг и выделение базовых признаков.
        """
        nickname_parts = self.preprocess_nickname(nickname)
        tokens = []
        for part in nickname_parts:
            # Пропускаем символы вроде "_"
            if part == "_":
                continue
            doc = self.nlp(part)
            for token in doc:
                tokens.append({
                    "text": token.text,       # Исходный текст
                    "lemma": token.lemma_,    # Лемма
                    "stem": self.stemmer.stem(token.text),  # Основа слова
                    "pos": token.pos_,       # Часть речи
                    "tag": token.tag_,       # Тег синтаксической роли
                })
        return tokens

    def classify_type(self, nickname):
        """
        Определение словообразовательного типа (номинативный, атрибутивный и т.д.).
        """
        nickname_parts = self.preprocess_nickname(nickname)
        if len(nickname_parts) > 1:
            return "составной"
        else:
            doc = self.nlp(nickname_parts[0])
            if doc[0].pos_ == "NOUN":
                return "номинативный"
            elif doc[0].pos_ == "ADJ":
                return "атрибутивный"
            elif doc[0].pos_ == "VERB":
                return "предикативный"
            else:
                return "неопределенный"

    def process_nicknames(self, nicknames):
        """
        Обработка списка никнеймов: анализ и классификация каждого.
        """
        results = []
        for nickname in nicknames:
            analysis = self.analyze(nickname)
            word_type = self.classify_type(nickname)
            results.append({
                "nickname": nickname,
                "analysis": analysis,
                "type": word_type
            })
        return results




