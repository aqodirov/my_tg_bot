from aiogram.fsm.state import State, StatesGroup

class ChatGPTInterfaceState(StatesGroup):
    waiting = State()

class PersonaState(StatesGroup):
    persona = State()
    recommendation = State()

class Person(StatesGroup):
    name = State()
    age = State()
    city = State()

class QuizState(StatesGroup):
    question_index = State()
    score = State()

class TranslatorState(StatesGroup):
    direction = State()
    text = State()

class RecommendationState(StatesGroup):
    waiting = State()


