import requests
from dotenv import load_dotenv
import os
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
import sqlite3
import asyncio

load_dotenv("API_KEY_waeth.env")
API_KEY = os.getenv("API_KEY")
api_key = API_KEY

load_dotenv("bot.env")  # Телеграмм
TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(bot=bot)


class WeatherQuery:
    def __init__(self, id, text, user_id):
        self.id = id
        self.text = text
        self.user_id = user_id

def get_weather_future(city, api_key):
    info_weather = ''
    url = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={city}&days=4&lang=ru"
    response = requests.get(url)
    data = response.json()

    if 'error' in data:
        return f"Ошибка API: {data['error']['message']}"

    today_date = data['forecast']['forecastday'][0]['date']
    temp = data['current']['temp_c']
    humidity = data['current'].get('humidity', 'Н/Д')
    wind_speed = data['current']['wind_kph']
    condition = data['current']['condition']['text']
    info_weather += f'Погода в городе {city} на сегодняшний день {today_date}: Температура: {temp}°C, Влажность: {humidity}%, Скорость ветра: {wind_speed} км/ч, Описание: {condition}\n'
    info_weather += '\n'

    forecast_day = data['forecast']['forecastday'][0]
    info_weather += f"Почасовой прогноз погоды в городе {city} на {today_date}:\n"
    for i, hour in enumerate(forecast_day['hour']):
        if i % 7 == 0:
            time = hour['time']
            temp_c = hour.get('temp_c', 'Н/Д')
            wind_kph = hour.get('wind_kph', 'Н/Д')
            condition = hour['condition']['text']
            info_weather += f"Время: {time}, Температура: {temp_c}°C, Скорость ветра: {wind_kph} км/ч, Описание: {condition}\n"
            info_weather += ' '
        info_weather += ' '

    info_weather += ' '
    if 'forecast' in data:
        for day in data['forecast']['forecastday']:
            date = day['date']
            temp_humidity = day['day'].get('avghumidity', 'Н/Д')
            temp_c = day['day'].get('avgtemp_c', 'Н/Д')
            condition = day['day']['condition']['text']
            wind_speed = day['day'].get('maxwind_kph', 'Н/Д')
            info_weather += f"Дата: {date}, Температура: {temp_c}°C, Влажность: {temp_humidity}%, Скорость ветра: {wind_speed} км/ч, Описание: {condition}\n"
            info_weather += '\n'
    else:
        info_weather += "Прогноз на несколько дней недоступен.\n"
    print(info_weather)

    return info_weather


async def send_message_to_user(user_id: int, message_text: str):
    try:
        await bot.send_message(chat_id=user_id, text=message_text)
        print(f"Сообщение отправлено пользователю {user_id}")
    except Exception as e:
        print(f"Ошибка при отправке сообщения: {e}")


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

async def main():
    while True:
        all_queries = await get_all_query()
        if all_queries:
            for query in all_queries:
                city = query.text
                user_id = query.user_id
                print(f"Обрабатываем запрос для города: {city}, пользователь: {user_id}")

                if user_id is None:
                    print(f"Пропущен запрос с ID {query.id}, так как user_id отсутствует.")
                    continue


                weather_info = get_weather_future(city, api_key)

                try:
                    await send_message_to_user(int(user_id), weather_info)
                    print(f"Сообщение отправлено пользователю {user_id}")
                except Exception as e:
                    print(f"Ошибка при отправке сообщения пользователю {user_id}: {e}")
                    continue

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

        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())