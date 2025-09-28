from services.openai_service import ask_gpt

STRICT_EN_RU = (
    "Ты — профессиональный переводчик EN→RU. Переводи строго и точно."
    " Никаких добавлений, пояснений, вопросов, приветствий."
    " Сохраняй пунктуацию, регистр, имена собственные и тон."
    " Если исходная фраза одно предложение — ответ тоже одно."
    " Выводи только перевод, без кавычек и слов вроде 'Перевод:'."
)
STRICT_RU_EN = (
    "You are a professional translator RU→EN. Translate strictly and faithfully."
    " Do not add or remove anything. Preserve punctuation, casing, names and tone."
    " If the source is one sentence, output one sentence."
    " Output translation only, no quotes, no extra words."
)

async def translate_text(text: str, direction: str) -> str:
    if direction == "en-ru":
        system_role = STRICT_EN_RU
    elif direction == "ru-en":
        system_role = STRICT_RU_EN
    else:
        system_role = "You are a precise translator. Output only the translation."
    prompt = text
    return await ask_gpt(prompt, system_role, model="gpt-4o-mini", temperature=0.1)
