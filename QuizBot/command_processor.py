# command_processor.py
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
from commands.start_command import StartCommand
from commands.help_command import HelpCommand
from commands.word_command import WordCommand
from commands.fact_command import FactCommand
from commands.progress_command import ProgressCommand
from commands.restart_command import RestartCommand
from answer_processor import handle_answer

class CommandProcessor:
    def __init__(self, application: Application):
        self.app = application

    def register_all(self):
        self.app.add_handler(CommandHandler("start", StartCommand.execute))
        self.app.add_handler(CommandHandler("help", HelpCommand.execute))
        self.app.add_handler(CommandHandler("word", WordCommand.execute))
        self.app.add_handler(CommandHandler("fact", FactCommand.execute))
        self.app.add_handler(CommandHandler("progress", ProgressCommand.execute))
        self.app.add_handler(CommandHandler("restart", RestartCommand.execute))
        self.app.add_handler(CallbackQueryHandler(handle_answer))

        # Один обработчик для всего текста (включая некорректные команды)
        self.app.add_handler(MessageHandler(filters.TEXT, self.handle_any_text))

    async def handle_any_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "Пожалуйста, используйте команды для взаимодействия с ботом:\n\n"
            "/start - приветствие\n"
            "/help - справка по командам\n"
            "/word - учить слова\n"
            "/fact - интересные факты\n"
            "/progress - ваш прогресс\n"
            "/restart - сбросить прогресс"
        )