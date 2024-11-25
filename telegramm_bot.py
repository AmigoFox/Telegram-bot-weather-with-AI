import asyncio
import sys
from typing import Any
from aiogram.handlers import MessageHandler
from dotenv import load_dotenv
import os
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

load_dotenv("bot.env")
TOKEN = os.getenv("BOT_TOKEN")

if TOKEN is None:
    print("Ошибка: BOT_TOKEN не найден в .env файле")
    sys.exit(1)

dp = Dispatcher()
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Привет, {html.bold(message.from_user.full_name)}, в каком городе хотите узнать погоду ?")

@dp.message()
async def echo_handler(message: Message) -> None:
    try:
        await message.send_copy(chat_id=TOKEN)
    except TypeError:
        await message.answer("Попробуй еще раз.")

async def main() -> None:
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

class MyHandler(MessageHandler):
    async def handle(self) -> Any:
        return self.event.text