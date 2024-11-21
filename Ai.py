import spacy
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
pd.set_option('display.max_columns', None)
nlp = spacy.load("ru_core_news_lg")
https = "https://rp5.ru/Погода_в_" # дальше для парсинга нужно тут указать город в НУЖНОМ ПАДЕЖЕ

name_city = pd.read_csv("A:/Language-processor/name_city.csv")
name_city.columns = name_city.columns.str.strip().str.lower()
print(name_city)

city = input("Погоду в каком городе хочешь посмотреть ?\n")
info = np.array([city])
info_df = pd.DataFrame(info.T, columns=['city'])

x = name_city['city']
y = name_city['city']


scaler = StandardScaler()
X_scaled = scaler.fit_transform(x)

info_scaled = scaler.transform(info_df)

model = LinearRegression()
model.fit(X_scaled, y)

predicted_city = model.predict(info_scaled)
print(predicted_city,"Это предсказанный город")