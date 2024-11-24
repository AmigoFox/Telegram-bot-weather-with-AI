import spacy
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import re
from sklearn.metrics import accuracy_score


nlp = spacy.load("ru_core_news_lg")
name_city = pd.read_csv("A:/Language-processor/name_city_extended.csv")
name_city.columns = name_city.columns.str.strip().str.lower()

city = input("Погоду в каком городе хочешь посмотреть ?\n")

words = re.findall(r'\b\w+\b', city.lower())
lemmas = []

for word in words:
    doc = nlp(word)
    if doc:
        lemma = doc[0].lemma_
        lemmas.append(lemma)

info = " ".join(lemmas)

name_city['city'] = name_city['city'].str.strip()
vectorizer = TfidfVectorizer()

X = vectorizer.fit_transform(name_city['city'])
y = name_city['city']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=400)

model = LogisticRegression(max_iter=15000)
model.fit(X_train, y_train)

info_vectorized = vectorizer.transform([info])

predicted_city = model.predict(info_vectorized)

print(f"Это предсказанный город: {predicted_city[0]}")

y_pred = model.predict(X_test)
print(f"Точность модели: {accuracy_score(y_test, y_pred)}")