# word_command.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import random

# Простой уровень: пары (русский, хорватский)
VOCAB_SIMPLE = [
    ("спасибо", "hvala"),
    ("пожалуйста", "molim"),
    ("привет", "bok"),
    ("дом", "kuća"),
    ("вода", "voda"),
    ("хлеб", "kruh"),
    ("день", "dan"),
    ("ночь", "noć"),
]

class WordCommand:
    @staticmethod
    async def execute(update: Update, context: ContextTypes.DEFAULT_TYPE):
        # Выбираем случайное слово
        ru, hr = random.choice(VOCAB_SIMPLE)

        # Случайно выбираем направление перевода
        if random.choice([True, False]):
            # Русский → Хорватский
            question = f"Переведи на хорватский:\n\n«{ru}»"
            correct = hr
            # Генерируем один неправильный вариант
            wrong = random.choice([w for w in [pair[1] for pair in VOCAB_SIMPLE] if w != hr])
        else:
            # Хорватский → Русский
            question = f"Переведи на русский:\n\n«{hr}»"
            correct = ru
            wrong = random.choice([w for w in [pair[0] for pair in VOCAB_SIMPLE] if w != ru])

        # Перемешиваем варианты
        options = [correct, wrong]
        random.shuffle(options)

        # Сохраняем правильный ответ в context для проверки
        context.user_data["correct_answer"] = correct

        # Создаём кнопки
        keyboard = [
            [InlineKeyboardButton(options[0], callback_data=options[0])],
            [InlineKeyboardButton(options[1], callback_data=options[1])],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(question, reply_markup=reply_markup)

async def handle_word_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # подтверждаем нажатие

    user_choice = query.data
    correct = context.user_data.get("correct_answer")

    if user_choice == correct:
        response = "✅ Правильно! Молодец! 🎉"
    else:
        response = f"❌ Неправильно.\nПравильный ответ: **{correct}**"

    # Отправляем результат
    await query.edit_message_text(response)