import requests
from dotenv import load_dotenv
import os
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
import sqlite3
import asyncio

# Загрузка переменных окружения
load_dotenv("API_KEY_waeth.env")
API_KEY = os.getenv("API_KEY")
api_key = API_KEY

load_dotenv("bot.env")  # Телеграмм
TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(bot=bot)

# Класс для хранения данных запроса
class WeatherQuery:
    def __init__(self, id, text, user_id):
        self.id = id
        self.text = text
        self.user_id = user_id

# Функция для получения всех запросов из базы данных
async def get_all_query():
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

# Функция для получения погоды
def get_weather_future(city, api_key):
    info_weather = ''
    url = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={city}&days=7&lang=ru"
    response = requests.get(url)
    data = response.json()

    if 'error' in data:
        return f"Ошибка API: {data['error']['message']}"
    today_date = data['forecast']['forecastday'][0]['date']
    temp = data['current']['temp_c']
    humidity = data['current']['humidity']
    wind_speed = data['current']['wind_kph']
    condition = data['current']['condition']['text']
    info_weather += f'Погода на сегодняшний день {today_date}: Температура: {temp}°C, Влажность: {humidity}%, Скорость ветра: {wind_speed} км/ч, Описание: {condition}\n'
    info_weather += '\n'

    if 'forecast' in data:
        for day in data['forecast']['forecastday']:
            date = day['date']
            humidity = data['current']['humidity']
            temp_c = day['day']['avgtemp_c']
            condition = day['day']['condition']['text']
            wind_speed = day['day']['maxwind_kph']
            info_weather += f"Дата: {date}, Температура: {temp_c}°C, Влажность: {humidity}%, Скорость ветра: {wind_speed} км/ч, Описание: {condition}\n"
            info_weather += '\n'
    else:
        info_weather += "Прогноз на несколько дней недоступен.\n"
        print(info_weather)
    return info_weather

# Асинхронная функция для отправки сообщения пользователю
async def send_message_to_user(user_id: int, message_text: str):
    try:
        await bot.send_message(chat_id=user_id, text=message_text)
        print(f"Сообщение отправлено пользователю {user_id}")
    except Exception as e:
        print(f"Ошибка при отправке сообщения: {e}")

# Основная асинхронная функция
async def main():
    while True:
        all_queries = await get_all_query()
        if all_queries:
            for query in all_queries:
                city = query.text
                user_id = query.user_id
                print(f"Обрабатываем запрос для города: {city}, пользователь: {user_id}")

                # Получаем погоду
                weather_info = get_weather_future(city, api_key)

                # Отправляем погоду пользователю
                await send_message_to_user(user_id, weather_info)

                # Удаляем обработанный запрос из базы данных
                conn = sqlite3.connect("weather_request.db")
                cursor = conn.cursor()
                try:
                    cursor.execute("DELETE FROM report WHERE id = ?", (query.id,))
                    conn.commit()
                    print(f"Запрос с ID {query.id} удален из базы данных.")
                except sqlite3.Error as e:
                    print(f"Ошибка при удалении запроса: {e}")
                finally:
                    conn.close()

        await asyncio.sleep(2)

if __name__ == "__main__":
    asyncio.run(main())
