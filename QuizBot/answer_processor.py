from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import telegram
from QuizBot.progress_manager import _progress, get_user_data
from QuizBot.progress_manager import save_progress, LEVELS
from QuizBot.tasks.vocab import VOCAB_RU_TO_HR, VOCAB_HR_TO_RU
from QuizBot.tasks.facts import FACTS

async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global _progress
    query = update.callback_query

    # Обрабатываем возможную ошибку "устаревшего" запроса
    try:
        await query.answer()
    except telegram.error.BadRequest as e:
        if "Query is too old" in str(e):
            # Игнорируем устаревшие запросы
            return
        else:
            # Пробрасываем другие ошибки
            raise

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

    # ПОЛУЧАЕМ ИСХОДНЫЙ ПОРЯДОК КНОПОК ИЗ СООБЩЕНИЯ
    original_keyboard = query.message.reply_markup.inline_keyboard
    original_options = []

    for row in original_keyboard:
        for button in row:
            # Извлекаем текст кнопки без эмодзи (если они есть)
            button_text = button.text
            # Убираем эмодзи чтобы получить чистый текст опции
            if button_text.startswith("✅ ") or button_text.startswith("❌ "):
                button_text = button_text[2:]
            original_options.append(button_text)

    # СОЗДАЕМ ОБНОВЛЕННУЮ КЛАВИАТУРУ СОХРАНЯЯ ИСХОДНЫЙ ПОРЯДОК
    new_keyboard = []

    for option in original_options:
        if option == user_choice:
            # Выделяем выбранную кнопку
            if user_choice == correct:
                button_text = "✅ " + option
            else:
                button_text = "❌ " + option
        elif option == correct and user_choice != correct:
            # Показываем правильный ответ зеленым, если пользователь ошибся
            button_text = "✅ " + option
        else:
            # Обычные кнопки
            button_text = option

        # Создаем кнопку с тем же callback_data что и в оригинале
        if is_word:
            callback_data = f"word|{direction}|{level}|{item_id}|{option}"
        else:
            callback_data = f"fact|{level}|{item_id}|{option}"

        new_keyboard.append([InlineKeyboardButton(button_text, callback_data=callback_data)])

    # Обновляем сообщение с новой клавиатурой
    try:
        await query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(new_keyboard))
    except Exception as e:
        print(f"Ошибка при обновлении клавиатуры: {e}")

    # ПРОВЕРЯЕМ ПРАВИЛЬНОСТЬ ОТВЕТА И ОБНОВЛЯЕМ ПРОГРЕСС
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

    await query.message.reply_text(msg, parse_mode="Markdown")