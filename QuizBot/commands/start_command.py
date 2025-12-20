# start_command.py
from telegram import Update
from telegram.ext import ContextTypes
from progress_manager import get_user_data, _progress

class StartCommand:
    @staticmethod
    async def execute(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = str(update.effective_user.id)
        get_user_data(_progress, user_id)

        await update.message.reply_text(
            "Я - бот для изучения хорватского языка 🇭🇷\n"
            "Напиши /help, чтобы увидеть справку.\n"
            "Напиши /word, чтобы начать учить слова.\n"
            "Напиши /fact, чтобы узнать интересный факт.\n"
            "Напиши /progress, чтобы посмотреть свой прогресс.\n"
            "Напиши /restart, чтобы сбросить весь прогресс."
        )