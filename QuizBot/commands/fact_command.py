# commands/fact_command.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
import random
from QuizBot.tasks.facts import FACTS
from QuizBot.progress_manager import _progress, get_user_data

class FactCommand:
    @staticmethod
    async def execute(update: Update, context):
        user_data = get_user_data(_progress, str(update.effective_user.id))
        facts = FACTS.get(user_data["level"], [])

        if not facts:
            await update.message.reply_text("Нет фактов.")
            return

        fact = random.choice(facts)
        options = [fact["correct"]] + fact["distractors"][:3]
        random.shuffle(options)

        keyboard = [[InlineKeyboardButton(o, callback_data=f"fact|{user_data['level']}|{facts.index(fact)}|{o}")] for o in options]

        await update.message.reply_text(f"Факт:\n\n{fact['question']}", reply_markup=InlineKeyboardMarkup(keyboard))