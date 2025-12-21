from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
from commands.start_command import StartCommand
from commands.help_command import HelpCommand
from commands.word_command import WordCommand
from commands.fact_command import FactCommand
from commands.progress_command import ProgressCommand
from commands.restart_command import RestartCommand
from answer_processor import handle_answer
from commands.reminder_command import ReminderCommand

class CommandProcessor:
    def __init__(self, application: Application):
        self.app = application  # сохраняем как self.app

    def register_all(self):
        self.app.add_handler(CommandHandler("start", StartCommand.execute))
        self.app.add_handler(CommandHandler("help", HelpCommand.execute))
        self.app.add_handler(CommandHandler("word", WordCommand.execute))
        self.app.add_handler(CommandHandler("fact", FactCommand.execute))
        self.app.add_handler(CommandHandler("progress", ProgressCommand.execute))
        self.app.add_handler(CommandHandler("restart", RestartCommand.execute))

        self.app.add_handler(CallbackQueryHandler(handle_answer, pattern=r"^(word|fact)\|"))
        self.app.add_handler(CallbackQueryHandler(handle_answer, pattern=r"^fact_advice\|"))
        self.app.add_handler(CallbackQueryHandler(ReminderCommand.handle_reminder_callback, pattern=r"^reminder_"))
        self.app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, self.handle_messages))

    async def handle_messages(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await HelpCommand.execute(update, context)