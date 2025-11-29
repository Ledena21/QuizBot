# commands/progress_command.py
from telegram import Update
from telegram.ext import ContextTypes
from QuizBot.tasks.vocab import VOCAB_RU_TO_HR  # ← используем один из словарей
from QuizBot.progress_manager import get_user_data, _progress

class ProgressCommand:
    @staticmethod
    async def execute(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = str(update.effective_user.id)
        user_data = get_user_data(_progress, user_id)

        level = user_data["level"]
        total_words_in_level = len(VOCAB_RU_TO_HR.get(level, []))
        learned_count = len(user_data["progress"].get(level, set()))

        total_correct = user_data["stats"]["total_correct"]
        total_attempts = user_data["stats"]["total_attempts"]
        accuracy = (total_correct / total_attempts * 100) if total_attempts > 0 else 0

        msg = (
            f"📊 Ваш прогресс:\n\n"
            f"🔹 Уровень: *{level}*\n"
            f"🔹 Выучено слов: *{learned_count}/{total_words_in_level}*\n"
            f"🔹 Точность: *{accuracy:.1f}%* ({total_correct}/{total_attempts})"
        )

        await update.message.reply_text(msg, parse_mode="Markdown")