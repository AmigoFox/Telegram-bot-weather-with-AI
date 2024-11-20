import spacy
import pandas as pd
nlp = spacy.load("ru_core_news_lg")
https = "https://rp5.ru/Погода_в_" # дальше для парсинга нужно тут указать город в НУЖНОМ ПАДЕЖЕ

name_city = pd.read_csv("name_city.csv")
print(name_city)

# для определение о каком городе идет речь

city = input("Погоду в каком городе хочешь посмотреть ? \n")
doc = nlp(city)
for token in doc:
    print(token.text)