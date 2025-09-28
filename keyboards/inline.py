from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
def info_inline():
    kb_list = [
        [
            InlineKeyboardButton(text='🎯 Случайный факт', callback_data='random_fact'),
            InlineKeyboardButton(text='💬 AI-чат', callback_data='chatgpt_interface')
        ],
        [
            InlineKeyboardButton(text='🎭 Диалог с личностью', callback_data='dialog_persona'),
            InlineKeyboardButton(text='🧠 Викторина', callback_data='quiz')
        ],
        [
            InlineKeyboardButton(text='🌍 Переводчик', callback_data='translator'),
            InlineKeyboardButton(text='🎬 Подборки и советы', callback_data='recommendations'),
        ]
    ]

    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard

def random_fact_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔁 Сгенерировать ещё", callback_data="random_fact_again")],
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_main_menu")]
        ]
    )

def persona_menu() -> InlineKeyboardMarkup:
    kb_list = [
        [
            InlineKeyboardButton(text="🧠 Эйнштейн", callback_data="persona_einstein"),
            InlineKeyboardButton(text="✒️ Шекспир", callback_data="persona_shakespeare")
        ],
        [
            InlineKeyboardButton(text="🚀 Илон Маск", callback_data="persona_musk"),
            InlineKeyboardButton(text="🎨 Да Винчи", callback_data="persona_davinci")
        ],
        [
            InlineKeyboardButton(text="🍭 Гарри Поттер", callback_data="persona_harry_potter"),
            InlineKeyboardButton(text="🤪 Джокер", callback_data="persona_joker")
        ],
        [
            InlineKeyboardButton(text="🤷‍♂️ Mr. Beast", callback_data="persona_mr_beast")
        ],
        [
            InlineKeyboardButton(text="⬅️ Назад", callback_data="back_main_menu")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb_list)

def quiz_keyboard(options: list) -> InlineKeyboardMarkup:
    kb_list = [[InlineKeyboardButton(text=opt, callback_data=f"quiz_answer_{opt}")]
               for opt in options]
    return InlineKeyboardMarkup(inline_keyboard=kb_list)

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def translator_menu():
    kb_list = [
        [InlineKeyboardButton(text="🇬🇧 EN → RU", callback_data="translate_en_ru")],
        [InlineKeyboardButton(text="🇷🇺 RU → EN", callback_data="translate_ru_en")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_main_menu")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb_list)

def back_button() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⬅️ Назад в главное меню", callback_data="back_main_menu")]
        ]
    )