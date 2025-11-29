from telegram.ext import Application
"""
Импортируем класс Application из модуля telegram.ext библиотеки python-telegram-bot. 
Application - объект, который обеспечивает взаимодействие нашего кода с телеграмом, 
через него бот подключается к телеграму, получает сообщения, вызывает команды, кнопки и т.д.
"""
from command_processor import CommandProcessor

class Bot:
    def __init__(this, token): # конструктор класса, this - ссылка на текущий экземпляр класса, token это очевидно токен
        this.application = Application.builder().token(token).build()
        """
        Application.builder() создаём строитель для объекта Application.
        .token(token) задаём токен бота.
        .build() собираем и возвращает готовый экземпляр Application.
        Результат сохраняется в атрибуте this.application, чтобы к нему можно было обратиться из других методов.
        """
        processor = CommandProcessor(this.application) # создаём экземпляр класса CommandProcessor, передавая ему this.application.
        processor.register_all() # вызываем метод register_all() у объекта processor

    def start_polling(this): # определяем метод start_polling
        print("Бот запущен.")
        this.application.run_polling() # опрос серверов телеграма