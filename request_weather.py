import sqlite3

import requests
import os
from dotenv import load_dotenv
import sqlite3

load_dotenv("API_KEY_waeth.env")
API_KEY = os.getenv("API_KEY")


class WeatherQuery:
    def __init__(self, id, text, user_id):
        self.id = id
        self.text = text
        self.user_id = user_id


def get_all_query():
    conn = sqlite3.connect("weather_request.db")
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM report")
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
        query_id = query.id
        text_to_process = query.text
        user_id = query.user_id
        print(query.id, text_to_process, query.user_id)
        text_city.append({
            'id': query_id,
            'text': text_to_process,
            'id_user' : user_id
        })
else:
    print("Ошибка при получении данных из базы данных.")

for i in text_city:
    print(i['id'],i['text'],i['id_user'])




'''
def get_weather(city, api_key):
    url = f'https://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&lang=ru'
    response = requests.get(url)
    data = response.json()
    if 'error' not in data:
        temp = data['current']['temp_c']
        humidity = data['current']['humidity']
        wind_speed = data['current']['wind_kph']
        condition = data['current']['condition']['text']
        return f'Погода на сегодня в городе {city}: {temp}°C, {condition}, влажность: {humidity}%, ветер: {wind_speed} км/ч.'
    else:
        return f'Не удалось получить данные для города {city}.'


def get_weather_future(city, api_key):
    url = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={city}&days=7&lang=ru"
    response = requests.get(url)
    data = response.json()

    # Создаем список для хранения прогнозов
    forecast_info = []

    for day in data['forecast']['forecastday']:
        date = day['date']
        temp_c = day['day']['avgtemp_c']
        condition = day['day']['condition']['text']
        forecast_info.append(f"Дата: {date}, Температура: {temp_c}°C, Описание: {condition}")

    # Возвращаем все прогнозы в виде строки
    return "\n".join(forecast_info)

if __name__ == "__main__":
    api_key = API_KEY
    city = "Ростов-на-Дону"
    get_weather(city, api_key)

api_key = API_KEY
city = 'Ростов-на-Дону'
print(get_weather(city, api_key))
print(get_weather_future(city, api_key))
'''