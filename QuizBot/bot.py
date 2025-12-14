# bot.py

import asyncio
from datetime import datetime
from telegram.ext import Application
from command_processor import CommandProcessor
from commands.reminder_command import ReminderCommand


class Bot:
    def __init__(self, token):
        self.application = Application.builder().token(token).build()
        self.processor = CommandProcessor(self.application)
        self.processor.register_all()

    async def _reminder_loop(self):
        """Фоновая задача: проверяет время и отправляет напоминания в заданные моменты."""
        # Укажите нужные времена здесь (час, минута)
        target_times = [
            (17, 50),   # 12:00
            (18, 0),   # 15:00
            (18, 10),  # 16:12 ← для отладки
            (18, 20),  # 17:30
            (18, 30),
            (19, 26),# 20:00
        ]
        last_sent = set()  # хранит (день, час, минута)

        while True:
            now = datetime.now()
            current_day = now.date()
            current_hour = now.hour
            current_minute = now.minute

            # Проверяем, совпадает ли текущее время с одним из целевых
            for hour, minute in target_times:
                if current_hour == hour and current_minute == minute:
                    key = (current_day, hour, minute)
                    if key not in last_sent:
                        print(f"[Напоминание] Отправка в {hour:02d}:{minute:02d}")
                        await self._send_reminders_to_all_users()
                        last_sent.add(key)
                        # Выходим, чтобы не отправлять несколько раз за минуту
                        break

            await asyncio.sleep(60)  # проверяем раз в минуту

    async def _send_reminders_to_all_users(self):
        """Отправляет напоминание всем пользователям из прогресса."""
        from progress_manager import _progress
        for user_id in _progress:
            try:
                await ReminderCommand.send_daily_reminder(self.application, user_id)
            except Exception as e:
                print(f"Не удалось отправить напоминание пользователю {user_id}: {e}")

    def start_polling(self):
        print("Бот запущен.")
        # Запускаем polling и фоновую задачу одновременно
        loop = asyncio.get_event_loop()
        loop.create_task(self._reminder_loop())
        self.application.run_polling()