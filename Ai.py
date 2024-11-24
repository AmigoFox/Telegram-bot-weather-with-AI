import spacy
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Загружаем модель spaCy для обработки русского языка
nlp = spacy.load("ru_core_news_lg")

# Загружаем данные с названиями городов
name_city = pd.read_csv("A:/Language-processor/name_city_extended.csv")
name_city.columns = name_city.columns.str.strip().str.lower()

# Вводим город для поиска погоды
city = input("Погоду в каком городе хочешь посмотреть ?\n")



doc = nlp(city)
doc_lemma = doc[0].lemma_
print(doc_lemma)# Используем lemma_


# Преобразуем лемму введённого города в массив
info = np.array([doc_lemma])

# Преобразуем введённый город в DataFrame
info_df = pd.DataFrame(info.T, columns=['city'])

# Убираем пробелы и лишние символы из данных
name_city['city'] = name_city['city'].str.strip()

# Создаем объект TfidfVectorizer для векторизации текста
vectorizer = TfidfVectorizer()

# Преобразуем названия городов в векторы с помощью TF-IDF
X = vectorizer.fit_transform(name_city['city'])

# Целевая переменная - это города, в которых будем искать сходства
y = name_city['city']

# Разделим данные на обучающие и тестовые наборы для тренировки модели
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=1)

# Обучаем модель логистической регрессии
model = LogisticRegression(max_iter=1411)
model.fit(X_train, y_train)

# Преобразуем вводимый город в тот же векторный формат
info_vectorized = vectorizer.transform(info_df['city'])

# Предсказываем город
predicted_city = model.predict(info_vectorized)

# Выводим результат
print(f"Это предсказанный город: {predicted_city[0]}")

# Проверка точности модели (по тестовым данным)
y_pred = model.predict(X_test)
print(f"Точность модели: {accuracy_score(y_test, y_pred)}")
