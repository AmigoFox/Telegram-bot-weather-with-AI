import spacy
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import re
from sklearn.metrics import accuracy_score
import sqlite3

class WeatherQuery:
    def __init__(self, id, text, user_id):
        self.id = id
        self.text = text
        self.user_id = user_id

def get_all_query():
    conn = sqlite3.connect('BD.db')
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM info_weather")
        rows = cursor.fetchall()
        queries = [WeatherQuery(row[0], row[1], row[2]) for row in rows]
        return queries
    except sqlite3.Error as e:
        print(f"Ошибка базы данных: {e}")
        return None
    finally:
        conn.close()

all_queries = get_all_query()

text_city = []
if all_queries:
    for query in all_queries:
        text_to_process = query.text
        print(query.id, text_to_process, query.user_id)
        text_city.append(text_to_process)
else:
    print("Ошибка при получении данных из базы данных.")
print(text_city)


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


def process_queries(queries):
    processed_queries = []
    for query in queries:
        processed_text = preprocess_text(query)
        print(f"Предобработанный текст: {processed_text}")


        doc = nlp(processed_text)
        lemmas = [token.lemma_ for token in doc]
        processed_queries.append(" ".join(lemmas))
    return processed_queries


def Ai_report(info):
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

processed_queries = process_queries(text_city)
for query in processed_queries:
    Ai_report(query)