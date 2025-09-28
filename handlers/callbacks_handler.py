from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery, Message
from messages.start_text import TEXT

# Тут я проимпортировал сервисы из пакета services
from services.openai_service import ask_gpt
from services.random_fact import get_fact
from services.recommendation_service import get_recommendation
from services.translator_service import translate_text
from services.personas import personas
from services.quiz_data import quiz_questions

# Здесь я проимпортировал inline клавиатуры
from keyboards.inline import (
    info_inline,
    persona_menu,
    translator_menu,
    quiz_keyboard,
    random_fact_menu
)

# Здесь я проимпортировал состояния, чтобы у меня шла непрерывная коммуникация
from states import PersonaState, QuizState, TranslatorState
from aiogram.fsm.state import StatesGroup, State

router = Router()

# Это блок моего кода про Случайный факт
@router.callback_query(F.data == "random_fact")
async def random_fact_callback(callback: CallbackQuery):
    await callback.answer("🎲 Генерирую факт...")
    fact = await get_fact()
    text = f"🐼 <b>Случайный факт:</b>\n\n{fact}"
    await callback.message.edit_text(text, reply_markup=random_fact_menu())

@router.callback_query(F.data == "random_fact_again")
async def random_fact_again_callback(callback: CallbackQuery):
    await callback.answer("🔁 Обновляю факт...")
    fact = await get_fact()
    text = f"🐼 <b>Случайный факт:</b>\n\n{fact}"
    await callback.message.edit_text(text, reply_markup=random_fact_menu())

@router.callback_query(F.data == "delete_fact_block")
async def delete_fact_block_callback(callback: CallbackQuery):
    await callback.message.edit_text(TEXT, reply_markup=info_inline())
    await callback.answer("↩️ Возврат в главное меню")

# Здесь у меня ChatGPT помощник / интерфейс
@router.callback_query(F.data == "chatgpt_interface")
async def chatgpt_interface_callback(callback: CallbackQuery):
    text = (
        "🤖 <b>ChatGPT-интерфейс</b>\n\n"
        "Ну как дела мой друг? Теперь можешь задать любой вопрос, а я помогу с ответом."
    )
    await callback.message.edit_text(text, reply_markup=callback.message.reply_markup)
    await callback.answer()

# Здесь у меня блок кода про выбор великой персоны для коммуникаии
@router.callback_query(F.data == "dialog_persona")
async def dialog_persona_callback(callback: CallbackQuery):
    await callback.message.edit_text(
        "🧠 Выбери, с кем хочешь побеседовать:",
        reply_markup=persona_menu()
    )
    await callback.answer()

# Здесь я возвращаю пользователя в главное меню
@router.callback_query(F.data == "back_main_menu")
async def back_main_menu_callback(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(TEXT, reply_markup=info_inline())
    await callback.answer()

# Здесь выбераем персону для коммуникации
@router.callback_query(F.data.startswith("persona_"))
async def choose_persona(callback: CallbackQuery, state: FSMContext):
    persona_key = callback.data.replace("persona_", "")
    persona_info = personas[persona_key]

    await state.set_state(PersonaState.persona)
    await state.update_data(persona_key=persona_key)

    await callback.message.edit_text(
        f"💬 Ты говоришь с {persona_info['name']}. Задай свой вопрос:",
        reply_markup=persona_menu()
    )
    await callback.answer()

# Здесь мой квиз
@router.callback_query(F.data == "quiz")
async def start_quiz(callback: CallbackQuery, state: FSMContext):
    await state.set_state(QuizState.question_index)
    await state.update_data(question_index=0, score=0)

    index = 0
    question_data = quiz_questions[index]
    text = f"🍭 <b>Вопрос №{index + 1}:</b> {question_data['question']}"

    await callback.message.edit_text(text, reply_markup=quiz_keyboard(question_data['options']))
    await callback.answer()

@router.callback_query(F.data.startswith("quiz_answer_"))
async def handle_answer(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    index = data["question_index"]
    score = data["score"]
    selected = callback.data.replace("quiz_answer_", "")
    correct_answer = quiz_questions[index]["answer"]

    if selected == correct_answer:
        score += 1
        await callback.answer("✅ Верно!", show_alert=False)
    else:
        await callback.answer(f"❌ Неверно! Правильный ответ: {correct_answer}", show_alert=False)

    index += 1
    if index < len(quiz_questions):
        await state.update_data(question_index=index, score=score)
        next_q = quiz_questions[index]
        text = f"🍭 <b>Вопрос №{index + 1}:</b> {next_q['question']}"
        await callback.message.edit_text(text, reply_markup=quiz_keyboard(next_q["options"]))
    else:
        total = len(quiz_questions)
        await callback.message.edit_text(
            f"🏁 Квиз завершён!\n\n<b>Твой результат:</b> {score}/{total}"
        )
        await state.clear()

# Тут реализация переводчика
@router.callback_query(F.data == "translator")
async def translator_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("🌐 Выбери направление перевода:", reply_markup=translator_menu())

@router.callback_query(F.data.startswith("translate_"))
async def choose_translation_direction(callback: CallbackQuery, state: FSMContext):
    direction = callback.data.replace("translate_", "").replace("_", "-")
    await state.set_state(TranslatorState.text)
    await state.update_data(direction=direction)
    await callback.message.edit_text("✍️ Введи текст, который нужно перевести:")
    await callback.answer()

@router.message(TranslatorState.text)
async def handle_translation(message: Message, state: FSMContext):
    data = await state.get_data()
    direction = data.get("direction")
    text_to_translate = message.text

    translated = await translate_text(text_to_translate, direction)
    await message.answer(f"✅ Перевод:\n\n{translated}")
    await state.clear()

#  Здесь реализация рекоммендаций
class RecommendationState(StatesGroup):
    waiting = State()

@router.callback_query(F.data == "recommendations")
async def recommendations_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("🎬 Введи, что хочешь: фильм, книгу, сериал или музыку:")
    await state.set_state(RecommendationState.waiting)
    await callback.answer()

@router.message(RecommendationState.waiting)
async def handle_recommendation(message: Message, state: FSMContext):
    reply = await get_recommendation(message.text)
    await message.answer(reply)
    await state.clear()

# Тут реализация рооевого диалога
@router.message(PersonaState.persona)
async def persona_conversation(message: Message, state: FSMContext):
    data = await state.get_data()
    persona_key = data.get("persona_key")

    if not persona_key:
        await message.answer("⚠️ Ошибка: персона не выбрана. Попробуй снова через /start")
        await state.clear()
        return

    persona = personas[persona_key]
    prompt = message.text

    reply = await ask_gpt(prompt, system_role=persona["system_role"])
    await message.answer(reply)

# общий ChatGPT, если нет коммуникации

@router.message(StateFilter(None))
async def chatgpt_text_handler(message: Message):
    user_text = message.text
    reply = await ask_gpt(
        user_text,
        system_role="Ты — дружелюбный ассистент, отвечай информативно и понятно."
    )
    await message.answer(reply)
