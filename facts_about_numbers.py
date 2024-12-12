import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from googletrans import Translator
import requests

from config import TOKEN


bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start_command(message: Message):
    await message.answer("Введите число, чтобы узнать интересный факт о нём!")


def translate_text_rus(eng_text):
    translator = Translator()
    rus_text = translator.translate(eng_text, src='en', dest='ru').text
    return rus_text


@dp.message()
async def get_about_number_fact(message: Message):
    number = message.text
    if number.isdigit():
        url = f'http://numbersapi.com/{number}'
        response = requests.get(url)
        if response.status_code == 200:
            info = translate_text_rus(response.text)
        else:
            info = f"Не удалось получить данные."
    else:
        info = f"'{number}' -это не число. Попробуйте снова."
    await message.answer(info)


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())