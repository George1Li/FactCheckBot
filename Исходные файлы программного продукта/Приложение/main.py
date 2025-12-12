import asyncio
import logging

import requests

import search
import prompts
from olama_commands import to_ollama
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command

import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

BOT_TOKEN =  os.environ.get("TOKEN")


logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
@dp.message(Command("1"))
async def cmd_start(message: types.Message):
    await message.answer(f"Ответ: <b>asddd</b>")
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    to_ollama("",1)
    await message.answer("Привет! Я бот анализирующий новости. Скинь мне новость и я проверю её в разных источниках")


@dp.message()
async def echo_handler(message: types.Message):
    if message.photo or message.video:
        msg_text = message.caption
        print(msg_text)
    else:
        msg_text = message.text
    if msg_text is None:
        await message.answer("Нет текста")
    else:
        print(msg_text)
        await message.answer(f"Новость в обработке")

        request = to_ollama(prompts.basic_prompt + msg_text + prompts.request_prompt, 0)
        print("Request: "+request)
        await message.answer("Request: "+request)

        search_result = search.compress_news(request)
        if search_result is None:
            await message.answer(f"Не удалось найти информацию по теме")
        else:
            print("Search result: "+search_result)
            req_text = prompts.basic_prompt + prompts.source_analysis_prompt + "Сама новость (её надо подтвердить или опровергнуть): "+msg_text +" Результаты поиска: " + search_result
            # for rt in range(len(req_text)//1024):
            #     await message.answer(f"Информация с сайтов" + req_text[rt*1024:(rt+1)*1024])
            # await message.answer(f"Информация с сайтов" + req_text[len(req_text)//1024 * 1024:-1])
            final_answer = to_ollama(req_text, 1)
            text = " " + final_answer
            await message.answer(f"Ответ: {text}")

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())