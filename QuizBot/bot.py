from telegram.ext import Application
from command_processor import CommandProcessor

class Bot:
    def __init__(self, token: str):
        self.application = Application.builder().token(token).build()
        processor = CommandProcessor(self.application)
        processor.register_all()

    def start_polling(self):  # ← НЕ async!
        print("Бот запущен. Нажмите Ctrl+C для остановки.")
        self.application.run_polling()  # ← без await!