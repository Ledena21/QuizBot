# commands/progress_command.py
from telegram import Update
from QuizBot.tasks.vocab import VOCAB_RU_TO_HR
from QuizBot.progress_manager import get_user_data, _progress

class ProgressCommand:
    @staticmethod
    async def execute(update: Update, context):
        user_data = get_user_data(_progress, str(update.effective_user.id))
        level = user_data["level"]

        learned = len(user_data["progress"].get(level, set()))
        total = len(VOCAB_RU_TO_HR.get(level, []))

        correct = user_data["stats"]["total_correct"]
        attempts = user_data["stats"]["total_attempts"]
        accuracy = correct / attempts * 100 if attempts else 0

        await update.message.reply_text(
            f"Ваш прогресс:\n\n"
            f"Уровень: *{level}*\n"
            f"Слова: *{learned}/{total}*\n"
            f"Точность: *{accuracy:.1f}%* ({correct}/{attempts})",
            parse_mode="Markdown"
        )