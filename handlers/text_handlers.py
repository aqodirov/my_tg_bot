from aiogram import Router, F
from aiogram.types import FSInputFile, Message
from keyboards.reply import start_keyboard

router = Router()

@router.message(F.text.casefold().in_(["привет","hi","hello"]))
async def text_handler(message: Message):
    await message.answer(f'Привет')

@router.message(F.text.lower().contains('как дела?'))
async def text_handler(message: Message):
    await message.answer(f"Всё отлично!")

@router.message(F.text.lower()=='файл')
async def file_handler(message: Message):
    doc =FSInputFile('compressed.pdf')
    await message.answer_document(doc)

@router.message(F.text.lower()== 'еда')
async def eat_handler(message: Message):
    await message.answer('Как будешь кушать котлетки?',reply_markup=start_keyboard())

@router.message(F.text=='С пюрешкой🍝')
async def potato_handler(message: Message):
    await message.answer("Оооо как вкусно!")
