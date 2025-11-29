# commands/fact_command.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import random
from QuizBot.tasks.facts import FACTS
from QuizBot.progress_manager import _progress, get_user_data

class FactCommand:
    @staticmethod
    async def execute(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        user_id = str(user.id)
        user_data = get_user_data(_progress, user_id)
        level = user_data["level"]

        facts = FACTS.get(level, [])
        if not facts:
            await update.message.reply_text("Нет фактов на этом уровне.")
            return

        fact_id = random.randrange(len(facts))
        fact = facts[fact_id]

        question = f"🧠 Интересный факт:\n\n{fact['question']}"
        correct = fact["correct"]
        distractors = fact["distractors"][:3]

        all_options = [correct] + distractors
        random.shuffle(all_options)

        # callback_data: fact|level|id|choice
        keyboard = []
        for opt in all_options:
            cb = f"fact|{level}|{fact_id}|{opt}"
            keyboard.append([InlineKeyboardButton(opt, callback_data=cb)])

        await update.message.reply_text(question, reply_markup=InlineKeyboardMarkup(keyboard))
