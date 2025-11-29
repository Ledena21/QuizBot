# commands/word_command.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from QuizBot.tasks.vocab import VOCAB_RU_TO_HR, VOCAB_HR_TO_RU
from QuizBot.progress_manager import _progress, get_user_data

@staticmethod
async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from QuizBot.progress_manager import save_progress, LEVELS
    from QuizBot.tasks.vocab import VOCAB_RU_TO_HR, VOCAB_HR_TO_RU
    from QuizBot.tasks.facts import FACTS

    global _progress
    query = update.callback_query
    await query.answer()

    user = update.effective_user
    user_id = str(user.id)
    user_data = get_user_data(_progress, user_id)

    data = query.data

    # Определяем тип контента и парсим данные
    if data.startswith("word|"):
        parts = data.split("|", 5)
        if len(parts) != 5:
            await query.edit_message_text("Ошибка данных (слово).")
            return

        _, direction, level, item_id_str, user_choice = parts
        item_id = int(item_id_str)

        # ИСПРАВЛЕНИЕ: используем direction для выбора словаря
        if direction == "ru_to_hr":
            vocab = VOCAB_RU_TO_HR
        else:  # direction == "hr_to_ru"
            vocab = VOCAB_HR_TO_RU

        source = vocab
        is_word = True

    elif data.startswith("fact|"):
        parts = data.split("|", 4)
        if len(parts) != 4:
            await query.edit_message_text("Ошибка данных (факт).")
            return

        _, level, item_id_str, user_choice = parts
        item_id = int(item_id_str)

        source = FACTS
        vocab = None
        is_word = False

    else:
        await query.edit_message_text("Неизвестный тип запроса.")
        return

    # ОБЩАЯ ЛОГИКА ПРОВЕРКИ ОТВЕТА
    if level not in source or item_id >= len(source[level]):
        await query.edit_message_text("Элемент не найден.")
        return

    correct = source[level][item_id]["correct"]

    # Обновляем статистику
    user_data["stats"]["total_attempts"] += 1

    if user_choice == correct:
        user_data["stats"]["total_correct"] += 1

        # ЛОГИКА ДЛЯ СЛОВ (прогресс и уровни)
        if is_word:
            user_data["progress"][level].add(item_id)
            total_words = len(vocab[level])

            if len(user_data["progress"][level]) == total_words:
                idx = LEVELS.index(level)
                if idx + 1 < len(LEVELS):
                    user_data["level"] = LEVELS[idx + 1]
                    msg = f"Уровень '{level}' завершён!\nТеперь вы на уровне: **{user_data['level'].upper()}**!"
                else:
                    msg = "Поздравляем! Вы выучили все слова!"
            else:
                msg = "Правильно!"
        else:
            msg = "Правильно!"
    else:
        msg = f"Неправильно.\nПравильный ответ: **{correct}**"

    save_progress(_progress)
    await query.edit_message_text(msg, parse_mode="Markdown")