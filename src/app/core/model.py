from transformers import BertForSequenceClassification

class BertModel:
    def __init__(self, num_labels, model_name='bert-base-uncased'):
        self.model = BertForSequenceClassification.from_pretrained(model_name, num_labels=num_labels)

    def get_model(self):
        return self.model
