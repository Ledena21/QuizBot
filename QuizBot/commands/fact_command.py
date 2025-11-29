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

    @staticmethod
    async def handle_fact_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
        global _progress
        query = update.callback_query
        await query.answer()

        user = update.effective_user
        user_id = str(user.id)
        user_data = get_user_data(_progress, user_id)

        data = query.data

        # Парсим callback_data
        if not data.startswith("fact|"):
            await query.edit_message_text("⚠️ Неверный формат данных.")
            return

        parts = data.split("|", 4)
        if len(parts) != 4:
            await query.edit_message_text("⚠️ Ошибка данных.")
            return

        _, level, fact_id_str, user_choice = parts
        fact_id = int(fact_id_str)

        # Получаем правильный ответ из FACTS
        if level not in FACTS or fact_id >= len(FACTS[level]):
            await query.edit_message_text("⚠️ Ошибка: факт не найден.")
            return

        correct = FACTS[level][fact_id]["correct"]

        # Обновляем статистику (только общую)
        user_data["stats"]["total_attempts"] += 1
        if user_choice == correct:
            user_data["stats"]["total_correct"] += 1
            msg = "✅ Правильно! Отлично знаете факты! 🎉"
        else:
            msg = f"❌ Неправильно.\nПравильный ответ: **{correct}**"

        from QuizBot.progress_manager import save_progress
        save_progress(_progress)
        await query.edit_message_text(msg, parse_mode="Markdown")