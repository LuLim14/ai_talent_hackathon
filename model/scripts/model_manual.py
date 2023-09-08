import pandas as pd
import numpy as np
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch, string, random
from torch.utils.data import Dataset, DataLoader


RANDOM_SEED = 42
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)
torch.manual_seed(RANDOM_SEED)
torch.random.manual_seed(RANDOM_SEED)
torch.cuda.random.manual_seed_all(RANDOM_SEED)
device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')


def preprocess_parameter(list_parameter):
    list_ABC = [x for x in string.ascii_uppercase]
    list_label = [x + '.' if x[-1] != '.' else x for x in list_parameter]
    list_label_pad = list_label + [tokenizer.pad_token]* (20 - len(list_label))
    s_option = ' '.join(['('+list_ABC[i]+') '+list_label_pad[i] for i in range(len(list_label_pad))])
    return s_option


def preprocess_sentiment(dict_sentiment):
    temp_dict = dict_sentiment.copy()
    for key, list_target in temp_dict.items():
        list_ABC = [x for x in string.ascii_uppercase]
        list_label = [x + '.' if x[-1] != '.' else x for x in list_target]
        list_label_pad = list_label + [tokenizer.pad_token]* (20 - len(list_label))
        temp_dict[key] = ' '.join(['('+list_ABC[i]+') '+list_label_pad[i] for i in range(len(list_label_pad))])
    return temp_dict


data = pd.read_excel('../../data-parsing/all_reviews.xlsx')
data[["service", "prices", "assortment", "quality", "cleanliness", "location"]] = 0

tokenizer = AutoTokenizer.from_pretrained("DAMO-NLP-SG/zero-shot-classify-SSTuning-XLM-R")
model = AutoModelForSequenceClassification.from_pretrained("DAMO-NLP-SG/zero-shot-classify-SSTuning-XLM-R")

for p in model.parameters():
    p.requires_grad = False
model.to(device).eval()

list_parameter = ["текст про персонал магазина", "текст про цены товаров", "текст про ассортимент товаров", "текст про качество товаров", "текст про чистоту магазина", "текст про расположение магазина"]
list_parameter_columns = ["service", "prices", "assortment", "quality", "cleanliness", "location"]
dict_sentiment = {0: ["сотрудники плохие", "сотрудники хорошие"],
                  1: ["товары дорогие", "товары дешёвые"],
                  2: ["ассортимент скудный", "ассортимент широкий"],
                  3: ["товары просроченные", "товары свежие"],
                  4: ["магазин грязный", "магазин чистый"],
                  5: ["расположение неудобное", "расположение удобное"]}
s_option_parameter = preprocess_parameter(list_parameter)
s_option_sentiment = preprocess_sentiment(dict_sentiment)

for i in data.index:
    parameter_ids = tokenizer(text=s_option_parameter + ' ' + tokenizer.sep_token + ' ' + data.loc[i, 'text'],
                              truncation=True,
                              padding=True,
                              max_length=512,
                              return_tensors='pt')['input_ids']
    parameter_ids = parameter_ids.to(device)
    parameter_logits = model(input_ids=parameter_ids).logits[:, :len(list_parameter)]
    parameter = torch.argmax(parameter_logits, dim=-1).item()
    sentiment_ids = tokenizer(text=s_option_sentiment[parameter] + ' ' + tokenizer.sep_token + ' ' + data.loc[i, 'text'],
                              truncation=True,
                              padding=True,
                              max_length=512,
                              return_tensors='pt')['input_ids']
    sentiment_ids = sentiment_ids.to(device)
    sentiment_logits = model(input_ids=sentiment_ids).logits[:, :2]
    sentiment = torch.argmax(sentiment_logits, dim=-1).item() * 2 - 1
    data.loc[i, list_parameter_columns[parameter]] = sentiment

data.to_csv('../data/all_reviews_manual.csv',
            index=False)