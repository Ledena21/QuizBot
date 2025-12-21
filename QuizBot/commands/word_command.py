# commands/word_command.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
import random
from tasks.vocab import VOCAB_RU_TO_HR, VOCAB_HR_TO_RU
from progress_manager import _progress, get_user_data
from telegram.ext import ContextTypes

class WordCommand:
    @staticmethod
    async def execute(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = str(update.effective_user.id)
        chat_id = update.effective_chat.id
        await WordCommand._send_word_question(context.bot, chat_id, user_id, "ru_to_hr")

    @staticmethod
    async def _send_word_question(bot, chat_id: int, user_id: str, direction: str):
        user_data = get_user_data(_progress, user_id)
        level = user_data["level"]
        vocab = VOCAB_RU_TO_HR if direction == "ru_to_hr" else VOCAB_HR_TO_RU
        words = vocab.get(level, [])
        if not words:
            await bot.send_message(chat_id=chat_id, text="Нет слов для этого уровня.")
            return

        learned = set(user_data["progress"][level])
        available = [i for i in range(len(words)) if i not in learned]
        if not available:
            await bot.send_message(chat_id=chat_id, text="Все слова выучены! Попробуйте следующий уровень.")
            return

        item_id = random.choice(available)
        item = words[item_id]

        options = [item["correct"]] + item["distractors"][:3]

        keyboard = []
        for idx in range(len(options)):
            callback_data = f"word|{direction}|{level}|{item_id}|{idx}"
            keyboard.append([InlineKeyboardButton(options[idx], callback_data=callback_data)])

        # Определяем текст вопроса
        question_text = item["question"]
        await bot.send_message(
            chat_id=chat_id,
            text=f"Слово:\n{question_text}",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )