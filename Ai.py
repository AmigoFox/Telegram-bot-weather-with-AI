import spacy
nlp = spacy.load("ru_core_news_lg")
https = "https://rp5.ru/Погода_в_" # дальше для парсинга нужно тут указать город в НУЖНОМ ПАДЕЖЕ

# для определение о каком городе идет речь
city_text = "city.txt"
print(city_text)

city = input("Погоду в каком городе хочешь посмотреть ? \n")
doc = nlp(city)
for token in doc:
    print(token.text)