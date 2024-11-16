import spacy
nlp = spacy.load("ru_core_news_lg")

city = input("Погоду в каком городе хочешь посмотреть ? \n")
doc = nlp(city)
for token in doc:
    print(token.text)