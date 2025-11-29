# commands/word_command.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
import random
from QuizBot.tasks.vocab import VOCAB_RU_TO_HR, VOCAB_HR_TO_RU
from QuizBot.progress_manager import _progress, get_user_data

class WordCommand:
    @staticmethod
    async def execute(update: Update, context):
        user_data = get_user_data(_progress, str(update.effective_user.id))
        level = user_data["level"]

        vocab, direction, text = random.choice([
            (VOCAB_RU_TO_HR, "ru_to_hr", "Переведи на хорватский:\n\n«"),
            (VOCAB_HR_TO_RU, "hr_to_ru", "Переведи на русский:\n\n«")
        ])

        words = vocab.get(level, [])
        if not words:
            await update.message.reply_text("Нет слов на этом уровне.")
            return

        learned = user_data["progress"][level]
        available = [i for i in range(len(words)) if i not in learned]

        if not available:
            await update.message.reply_text("Вы выучили все слова!")
            return

        word_id = random.choice(available)
        word = words[word_id]

        options = [word["correct"]] + word["distractors"][:3]
        random.shuffle(options)

        keyboard = [
            [InlineKeyboardButton(opt, callback_data=f"word|{direction}|{level}|{word_id}|{opt}")]
            for opt in options
        ]

        await update.message.reply_text(
            f"{text}{word['question']}»",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )