import spacy
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import re
from sklearn.metrics import accuracy_score
import sqlite3

from torchgen.api.cpp import return_type


def get_query_info(id, text, id_user):
    conn = sqlite3.connect('BD.db') # Подключение к базе данных
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM info_weather WHERE id = ?", (id, text, id_user,))  # Запрос к БД
        query_data = cursor.fetchone()
        if query_data:
            return {
                "id": query_data[0],
                "text": query_data[1],
                "id_user": query_data[2],
            }
        else:
            return None
    except sqlite3.Error as e:
        print(f"Ошибка базы данных: {e}")
        return None
    finally:
        conn.close()


nlp = spacy.load("ru_core_news_lg")


name_city = pd.read_csv("A:/Language-processor/name_city_extended.csv")
name_city.columns = name_city.columns.str.strip().str.lower()
name_city['city'] = name_city['city'].str.strip()


stop_words = {"какая", "погода", "в", "для", "в каком", "когда", "по", "что", "город", "это", "вопрос", "на", "вопросе"}


def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zа-яё ]', '', text)  # Удаляем все неалфавитные символы
    words = text.split()
    words = [word for word in words if word not in stop_words]
    return " ".join(words)


city = preprocess_text(input("Погоду в каком городе хочешь посмотреть ?\n"))
words = re.findall(r'\b\w+\b', city.lower())
lemmas = [nlp(word)[0].lemma_ for word in words]

info = " ".join(lemmas)

vectorizer = TfidfVectorizer(ngram_range=(1, 2), max_features=5000)
X = vectorizer.fit_transform(name_city['city'])
y = name_city['city']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=400)

model = LogisticRegression(max_iter=1500, C=3.0, solver='liblinear')
model.fit(X_train, y_train)

info_vectorized = vectorizer.transform([info])
predicted_city = model.predict(info_vectorized)

print(f"Это предсказанный город: {predicted_city[0]}")

y_pred = model.predict(X_test)
print(f"Точность модели: {accuracy_score(y_test, y_pred)}")