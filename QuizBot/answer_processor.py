# answer_processor.py

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import telegram
from progress_manager import _progress, get_user_data, save_progress, LEVELS
from tasks.vocab import VOCAB_RU_TO_HR, VOCAB_HR_TO_RU
from tasks.facts import FACTS
from commands.reminder_command import ReminderCommand  # ← для отправки следующего вопроса


async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global _progress
    query = update.callback_query

    try:
        await query.answer()
    except telegram.error.BadRequest as e:
        if "Query is too old" in str(e):
            return
        else:
            raise

    user_id = str(update.effective_user.id)
    user_data = get_user_data(_progress, user_id)
    data = query.data

    if data.startswith("word|"):
        parts = data.split("|", 5)
        if len(parts) != 5:
            await query.edit_message_text("Ошибка данных (слово).")
            return
        _, direction, level, item_id_str, user_choice = parts
        item_id = int(item_id_str)
        vocab = VOCAB_RU_TO_HR if direction == "ru_to_hr" else VOCAB_HR_TO_RU
        is_word = True
        source = vocab

    elif data.startswith("fact|"):
        parts = data.split("|", 4)
        if len(parts) != 4:
            await query.edit_message_text("Ошибка данных (факт).")
            return
        _, level, item_id_str, user_choice = parts
        item_id = int(item_id_str)
        source = FACTS
        is_word = False
        vocab = None

    else:
        await query.edit_message_text("Неизвестный тип запроса.")
        return

    if level not in source or item_id >= len(source[level]):
        await query.edit_message_text("Элемент не найден.")
        return

    correct_answer = source[level][item_id]["correct"]
    user_data["stats"]["total_attempts"] += 1

    # Получаем исходные опции
    original_keyboard = query.message.reply_markup.inline_keyboard
    original_options = []
    for row in original_keyboard:
        for button in row:
            text = button.text
            if text.startswith("✅ ") or text.startswith("❌ "):
                text = text[2:]
            original_options.append(text)

    # Создаём обновлённую клавиатуру
    new_keyboard = []
    for option in original_options:
        if option == user_choice:
            btn_text = "✅ " + option if user_choice == correct_answer else "❌ " + option
        elif option == correct_answer and user_choice != correct_answer:
            btn_text = "✅ " + option
        else:
            btn_text = option

        if is_word:
            callback_data = f"word|{direction}|{level}|{item_id}|{option}"
        else:
            callback_data = f"fact|{level}|{item_id}|{option}"
        new_keyboard.append([InlineKeyboardButton(btn_text, callback_data=callback_data)])

    try:
        await query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(new_keyboard))
    except Exception as e:
        print(f"Ошибка обновления клавиатуры: {e}")

    # === ОБНОВЛЯЕМ СТАТИСТИКУ ===
    is_correct = (user_choice == correct_answer)
    if is_correct:
        user_data["stats"]["total_correct"] += 1
        if is_word:
            user_data["progress"][level].add(item_id)
            total_words = len(vocab[level])
            if len(user_data["progress"][level]) == total_words:
                idx = LEVELS.index(level)
                if idx + 1 < len(LEVELS):
                    user_data["level"] = LEVELS[idx + 1]
                # msg будет обработан ниже, если не в сессии
        # msg для обычного режима
        msg = "Правильно!"
    else:
        msg = f"Неправильно.\nПравильный ответ: **{correct_answer}**"

    save_progress(_progress)

    # === ПРОВЕРКА: В СЕССИИ ТЕСТА? ===
    session = user_data.get("test_session")
    if session is not None:
        # Обновляем счётчик правильных ответов
        if is_correct:
            session["correct_count"] += 1
        session["current"] += 1
        save_progress(_progress)

        # Отправляем следующий вопрос (или завершаем)
        await ReminderCommand._send_next_test_question(
            context.bot,
            update.effective_chat.id,
            user_id
        )
    else:
        # Обычный режим — показываем результат
        await query.message.reply_text(msg, parse_mode="Markdown")