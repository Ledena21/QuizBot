# commands/fact_command.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
import random
from tasks.facts import FACTS
from progress_manager import _progress, get_user_data
from telegram.ext import ContextTypes

class FactCommand:
    @staticmethod
    async def execute(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Вызывается как команда /fact (через сообщение)."""
        user_id = str(update.effective_user.id)
        chat_id = update.effective_chat.id
        await FactCommand._send_fact_question(context.bot, chat_id, user_id)

    @staticmethod
    async def _send_fact_question(bot, chat_id: int, user_id: str):
        """Основная логика — отправка факта по chat_id и user_id."""
        user_data = get_user_data(_progress, user_id)
        facts = FACTS.get(user_data["level"], [])

        if not facts:
            await bot.send_message(chat_id=chat_id, text="Нет фактов.")
            return

        fact = random.choice(facts)
        options = [fact["correct"]] + fact["distractors"][:3]
        random.shuffle(options)

        fact_index = FACTS[user_data["level"]].index(fact)
        keyboard = [
            [InlineKeyboardButton(o, callback_data=f"fact|{user_data['level']}|{fact_index}|{o}")]
            for o in options
        ]

        await bot.send_message(
            chat_id=chat_id,
            text=f"Факт:\n\n{fact['question']}",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )