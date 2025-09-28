import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties

from config import TOKEN
from handlers import router
import logging

#FSM

async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
    dp = Dispatcher()  # Создаём диспетчер, который будет ловить события: команды (/start), сообщения, нажатия кнопок и т.д.
    dp.include_router(router)
    await dp.start_polling(bot)

asyncio.run(main())
