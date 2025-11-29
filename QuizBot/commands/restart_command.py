from telegram import Update
from telegram.ext import ContextTypes
from QuizBot.progress_manager import _progress, save_progress

class RestartCommand:
    @staticmethod
    async def execute(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = str(update.effective_user.id)
        if user_id in _progress:
            del _progress[user_id]
            save_progress(_progress)
        await update.message.reply_text("Ваш прогресс сброшен.\nМожете начать заново с команды /word или /fact.")