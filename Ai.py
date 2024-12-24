import sqlite3
import time
import spacy
from g4f.client import Client as G4FClient
from g4f import models
import re
import asyncio
from datetime import datetime
import pandas as pd
from io import StringIO
import sys

# Устанавливаем политику событийного цикла для Windows
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

nlp = spacy.load("ru_core_news_lg")
pd.set_option('display.max_colwidth', None)

def send_request(text, prompt, model):
    try:
        client = G4FClient()
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": f'{prompt}\n{text}'
                }
            ]
        )
        return {'result': response.choices[0].message.content}
    except Exception as e:
        return {'error': str(e)}

def answer(text: str, prompt: str, model: str = 'gpt-4o', limit: int = 60, timeout: int = 100) -> str:
    result = send_request(text, prompt, model)

    if 'error' in result:
        print(f"Ошибка при обработке запроса: {result['error']}")
        return None

    res = result['result']
    clear_text = re.sub(r"[A-Za-z]", "", res)
    clear_text = re.sub(r'\s+', ' ', clear_text.strip())

    if len(clear_text) > limit:
        res = res.strip()
        index = res.find('.ai')

        if index > 0:
            res = res[index + 3:]
            return res
        else:
            return res
    else:
        return None

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

def main():
    while True:
        all_queries = get_all_query()
        text_city = []

        if all_queries:
            for query in all_queries:
                query_id = query.id
                text_to_process = query.text
                user_id = query.user_id
                print(f"Обрабатываем запрос для города: {text_to_process}, пользователь: {user_id}")
                text_city.append({
                    'id': query_id,
                    'text': text_to_process,
                    'id_user': user_id
                })
        else:
            print("Ошибка при получении данных из базы данных.")

        if all_queries:
            for query in all_queries:
                print(f'вот вот это {query} вот запос ')
                if __name__ == '__main__':
                    result = answer(
                        prompt= 'Напиши название города в России. Оно может быть неформальное или в виде аббревиатуры. Ответь только названием города в официальном виде. Если не знаешь - ответь 0',
                        text= query.text,
                        limit= 1
                    )
                    if result is not None:
                        conn_req = sqlite3.connect("weather_request.db")
                        cursor = conn_req.cursor()
                        cursor.execute(
                            '''
                            INSERT INTO report (text, id_user) 
                            VALUES (?, ?)
                                ''', (result, query.user_id))  # Добавляем id_user
                        conn_req.commit()
                        conn_req.close()
                        print(f"Результат '{result}' добавлен в базу данных для запроса с ID {query.id}.")

                        # Удаляем запрос из базы данных BD.db
                        conn_bd = sqlite3.connect("BD.db")
                        cursor_bd = conn_bd.cursor()
                        try:
                            cursor_bd.execute("DELETE FROM info_weather WHERE id = ?", (query.id,))
                            conn_bd.commit()
                            print(f"Запрос с ID {query.id} удален из базы данных BD.db.")
                        except sqlite3.Error as e:
                            print(f"Ошибка при удалении запроса из базы данных BD.db: {e}")
                        finally:
                            conn_bd.close()
                    else:
                        print(f"Результат для запроса с ID {query.id} не получен.")

        print("Ожидание 5 секунд перед следующим запуском...")
        time.sleep(1)

if __name__ == "__main__":
    main()