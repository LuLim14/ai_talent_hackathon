import pandas as pd
import numpy as np
from transformers import pipeline
import torch, string, random
from torch.utils.data import Dataset, DataLoader

RANDOM_SEED = 42
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)
torch.manual_seed(RANDOM_SEED)
torch.random.manual_seed(RANDOM_SEED)
torch.cuda.random.manual_seed_all(RANDOM_SEED)
device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')

data = pd.read_excel('../../data-parsing/all_reviews.xlsx')
data[["service", "prices", "assortment", "quality", "cleanliness", "location"]] = 0


classifier = pipeline("zero-shot-classification",
                      model="mjwong/multilingual-e5-large-xnli-anli",
                      tokenizer="mjwong/multilingual-e5-large-xnli-anli",
                      device=0)

list_parameter = ["персонал магазина", "цены товаров", "ассортимент товаров", "качество товаров", "чистота магазина",
                  "расположение магазина"]
dict_sentiment = {"персонал магазина": ["сотрудники плохие", "сотрудники хорошие"],
                  "цены товаров": ["товары дорогие", "товары дешёвые"],
                  "ассортимент товаров": ["ассортимент скудный", "ассортимент широкий"],
                  "качество товаров": ["товары просроченные", "товары свежие"],
                  "чистота магазина": ["магазин грязный", "магазин чистый"],
                  "расположение магазина": ["расположение неудобное", "расположение удобное"]}
dict_parameter = {"персонал магазина": "service",
                  "цены товаров": "prices",
                  "ассортимент товаров": "assortment",
                  "качество товаров": "quality",
                  "чистота магазина": "cleanliness",
                  "расположение магазина": "location"}


for i in data.index:
    parameter = classifier(data.loc[i, 'text'],
                           list_parameter,
                           hypothesis_template="текст про {}")['labels'][0]
    sentiment = classifier(data.loc[i, 'text'],
                           dict_sentiment[parameter],
                           hypothesis_template="в тексте {}")['labels'][0]
    data.loc[i, dict_parameter[parameter]] = dict_sentiment[parameter].index(sentiment) * 2 - 1


data.to_csv('../data/all_reviews_manual.csv',
            index=False)