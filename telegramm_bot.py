import asyncio
import sys
import logging
from dotenv import load_dotenv
import os
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
import sqlite3

load_dotenv("bot.env")
TOKEN = os.getenv("BOT_TOKEN")
logging.basicConfig(level=logging.INFO)

CON = "BD.db"

if TOKEN is None:
    print("Ошибка: BOT_TOKEN не найден в .env файле")
    sys.exit(1)

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(bot=bot)


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Привет, {html.bold(message.from_user.full_name)}, в каком городе хотите узнать погоду ?")

async def main() -> None:
    await dp.start_polling(bot)


@dp.message()
async def log_message(message: Message):
       if not message.from_user.is_bot:  # Проверяем, что сообщение не от бота
            print(message.text)
            add_query(CON, message.text, message.from_user.id)
       else:
             print(f"Получено сообщение от бота: {message.text}")


def add_query(db_file, query, id_user):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO info_weather (text, id_user) VALUES (?, ?)", (query, id_user))
        conn.commit()
        return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"Ошибка при добавлении запроса: {e}")
    finally:
        conn.close()


if __name__ == "__main__":
    asyncio.run(main())