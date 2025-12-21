from telegram import Update
from telegram.ext import ContextTypes
from tasks.vocab import VOCAB_RU_TO_HR
from progress_manager import get_user_data, _progress

class ProgressCommand:
    @staticmethod
    async def execute(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = str(update.effective_user.id)
        user_data = get_user_data(_progress, user_id)
        level = user_data["level"]

        learned = len(user_data["progress"].get(level, set()))
        total = len(VOCAB_RU_TO_HR.get(level, []))

        correct = user_data["stats"]["total_correct"]
        attempts = user_data["stats"]["total_attempts"]
        accuracy = correct / attempts * 100 if attempts else 0
        streak_days = user_data.get("reminder_streak_days", 0)

        await update.message.reply_text(
            f"Ваш прогресс:\n\n"
            f"Уровень: *{level}*\n"
            f"Слова: *{learned}/{total}*\n"
            f"Точность: *{accuracy:.1f}%* ({correct}/{attempts})\n"
            f"Серия дней без пропусков: *{streak_days}* дней",
            parse_mode="Markdown"
        )