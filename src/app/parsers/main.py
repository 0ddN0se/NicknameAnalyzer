from src.app.core.datapreprocessor import DataPreprocessor

# preprocessor = DataPreprocessor(
#     input_path="src/data/dataset/nicknames.json",
#     output_path="src/data/dataset/processed_nicknames.json"
# )
# preprocessor.preprocess_data()
# print("Предобработка завершена. Данные сохранены в processed_nicknames.json.")

preprocessor = DataPreprocessor(
    input_path="src/data/dataset/vkdata.json",
    output_path="src/data/dataset/processed_vkdata.json"
)
preprocessor.preprocess_data()
print("Предобработка завершена. Данные сохранены в processed_vkdata.json.")




