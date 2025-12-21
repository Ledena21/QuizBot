from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.error import BadRequest
from progress_manager import _progress, get_user_data, save_progress, LEVELS
from commands.word_command import WordCommand
from commands.fact_command import FactCommand
import random


class ReminderCommand:
    @staticmethod
    async def send_daily_reminder(application, user_id: str):
        bot = application.bot
        user_data = get_user_data(_progress, user_id)
        streak = user_data.get("reminder_streak_days", 0)
        skip_count = user_data.get("reminder_skip_count", 0)
        message = (
            f"Время учиться!\n"
            f"Уровень: {user_data['level'].upper()}\n"
            f"Серия дней без пропусков: {streak} дней\n"
            f"Пропусков сегодня: {skip_count}/3\n"
            f"Нажмите кнопку ниже, чтобы начать тест:"
        )
        keyboard = [
            [InlineKeyboardButton("Пройти тест", callback_data="reminder_start")],
            [InlineKeyboardButton("Пропустить", callback_data="reminder_skip")]
        ]
        try:
            await bot.send_message(
                chat_id=int(user_id),
                text=message,
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        except Exception as e:
            print(f"[Напоминание] Ошибка отправки пользователю {user_id}: {e}")

    @staticmethod
    async def handle_reminder_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        try:
            await query.answer()
        except BadRequest as e:
            if "Query is too old" in str(e) or "query id is invalid" in str(e):
                return
            else:
                raise
        user_id = str(update.effective_user.id)
        chat_id = query.message.chat_id
        bot = context.bot
        user_data = get_user_data(_progress, user_id)

        if query.data == "reminder_start":
            user_data["reminder_skip_count"] = 0
            today = datetime.now().date().isoformat()
            last_active = user_data.get("reminder_last_active")
            if last_active == today:
                pass
            elif last_active == (datetime.now() - timedelta(days=1)).date().isoformat():
                user_data["reminder_streak_days"] += 1
            else:
                user_data["reminder_streak_days"] = 1
            user_data["reminder_last_active"] = today

            # Инициализируем сессию теста
            user_data["test_session"] = {
                "type": "reminder_test",
                "current": 0,
                "total": 5,
                "correct_count": 0
            }
            save_progress(_progress)
            await ReminderCommand._send_next_test_question(bot, chat_id, user_id)
            await query.edit_message_text("Тест начат.")

        elif query.data == "reminder_skip":
            user_data["reminder_skip_count"] += 1
            skip_count = user_data["reminder_skip_count"]
            if skip_count >= 3:
                # Сбрасываем счётчик пропусков
                user_data["reminder_skip_count"] = 0
                user_data["reminder_streak_days"] = 0
                user_data["reminder_last_active"] = None

                if user_data["level"] != "beginner":
                    idx = LEVELS.index(user_data["level"])
                    user_data["level"] = LEVELS[idx - 1]
                    user_data["progress"][user_data["level"]] = set()
                    msg = f"3 пропуска подряд. Уровень снижен до **{user_data['level'].upper()}**."
                else:
                    msg = "3 пропуска подряд. Остаётесь на уровне **BEGINNER**."
            else:
                msg = f"Пропущено. Пропусков: {skip_count}/3"
            await query.edit_message_text(msg, parse_mode="Markdown")
            save_progress(_progress)

    @staticmethod
    async def _send_next_test_question(bot, chat_id: int, user_id: str):
        user_data = get_user_data(_progress, user_id)
        session = user_data.get("test_session")
        if not session or session["current"] >= session["total"]:
            correct = session["correct_count"]
            total = session["total"]
            user_data.pop("test_session", None)
            save_progress(_progress)
            await bot.send_message(
                chat_id=chat_id,
                text=f"Тест завершён!\nВы ответили правильно на **{correct} из {total}** вопросов.",
                parse_mode="Markdown"
            )
            from tasks.vocab import VOCAB_RU_TO_HR
            level = user_data["level"]
            learned = len(user_data["progress"].get(level, set()))
            total_words = len(VOCAB_RU_TO_HR.get(level, []))
            correct_stats = user_data["stats"]["total_correct"]
            attempts = user_data["stats"]["total_attempts"]
            accuracy = correct_stats / attempts * 100 if attempts else 0
            streak_days = user_data.get("reminder_streak_days", 0)
            progress_text = (
                f"Ваш прогресс:\n"
                f"Уровень: *{level}*\n"
                f"Слова: *{learned}/{total_words}*\n"
                f"Точность: *{accuracy:.1f}%* ({correct_stats}/{attempts})\n"
                f"Серия дней без пропусков: *{streak_days}* дней"
            )
            await bot.send_message(
                chat_id=chat_id,
                text=progress_text,
                parse_mode="Markdown"
            )
            return

        question_index = session["current"]
        if question_index < 4:
            rand = random.randint(1, 10)
            direction = "ru_to_hr" if rand > 5 else "hr_to_ru"
            await WordCommand._send_word_question(bot, chat_id, user_id, direction)
        else:
            await FactCommand._send_fact_question(bot, chat_id, user_id)