# commands/word_command.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
import random
from tasks.vocab import VOCAB_RU_TO_HR, VOCAB_HR_TO_RU
from progress_manager import _progress, get_user_data
from telegram.ext import ContextTypes

class WordCommand:
    @staticmethod
    async def execute(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Вызывается как команда /word (через сообщение)."""
        user_id = str(update.effective_user.id)
        chat_id = update.effective_chat.id
        await WordCommand._send_word_question(context.bot, chat_id, user_id)

    @staticmethod
    async def _send_word_question(bot, chat_id: int, user_id: str):
        """Основная логика — отправка вопроса по chat_id и user_id."""
        user_data = get_user_data(_progress, user_id)
        level = user_data["level"]

        vocab, direction, text = random.choice([
            (VOCAB_RU_TO_HR, "ru_to_hr", "Переведи на хорватский:\n\n«"),
            (VOCAB_HR_TO_RU, "hr_to_ru", "Переведи на русский:\n\n«")
        ])

        words = vocab.get(level, [])
        if not words:
            await bot.send_message(chat_id=chat_id, text="Нет слов на этом уровне.")
            return

        learned = user_data["progress"][level]
        available = [i for i in range(len(words)) if i not in learned]
        if not available:
            await bot.send_message(chat_id=chat_id, text="Вы выучили все слова!")
            return

        word_id = random.choice(available)
        word = words[word_id]

        options = [word["correct"]] + word["distractors"][:3]
        random.shuffle(options)

        keyboard = [
            [InlineKeyboardButton(opt, callback_data=f"word|{direction}|{level}|{word_id}|{opt}")]
            for opt in options
        ]

        await bot.send_message(
            chat_id=chat_id,
            text=f"{text}{word['question']}»",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )