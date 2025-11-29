# commands/word_command.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import random
from QuizBot.tasks.vocab import VOCAB_RU_TO_HR, VOCAB_HR_TO_RU
from QuizBot.progress_manager import _progress, get_user_data

class WordCommand:
    @staticmethod
    async def execute(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        user_id = str(user.id)
        user_data = get_user_data(_progress, user_id)
        level = user_data["level"]

        # Случайный выбор направления перевода
        if random.choice([True, False]):
            vocab = VOCAB_RU_TO_HR
            direction = "ru_to_hr"
            prefix = "Переведи на хорватский:\n\n«"
            suffix = "»"
        else:
            vocab = VOCAB_HR_TO_RU
            direction = "hr_to_ru"
            prefix = "Переведи на русский:\n\n«"
            suffix = "»"

        words = vocab.get(level, [])
        if not words:
            await update.message.reply_text("Нет слов на этом уровне.")
            return

        learned = user_data["progress"][level]
        available = [i for i in range(len(words)) if i not in learned]

        if not available:
            await update.message.reply_text("Вы выучили все слова этого уровня!")
            return

        word_id = random.choice(available)
        word = words[word_id]

        question = f"{prefix}{word['question']}{suffix}"
        correct = word["correct"]
        distractors = word["distractors"][:3]

        all_options = [correct] + distractors
        random.shuffle(all_options)

        # ← ВАЖНО: callback_data с префиксом word|
        keyboard = []
        for opt in all_options:
            cb = f"word|{direction}|{level}|{word_id}|{opt}"
            keyboard.append([InlineKeyboardButton(opt, callback_data=cb)])

        await update.message.reply_text(question, reply_markup=InlineKeyboardMarkup(keyboard))