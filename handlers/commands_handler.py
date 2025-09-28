from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import Command
from keyboards.inline import info_inline
from keyboards.reply import start_keyboard
from messages.start_text import TEXT


router = Router()

@router.message(Command("start"))
async def start_handler(message: Message):
    await message.answer(TEXT, reply_markup=info_inline())

