import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
from task_db import add_task, get_tasks, delete_task

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Надішли мені завдання, і я його збережу.\nЩоб побачити список, напиши /tasks")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id
    text = update.message.text
    add_task(user_id, text)
    await update.message.reply_text("Завдання додано! Напиши /tasks щоб переглянути.")

async def show_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id
    tasks = get_tasks(user_id)

    if not tasks:
        await update.message.reply_text("Немає завдань.")
        return

    keyboard = []
    for task_id, task_text in tasks:
        # Створюємо кнопку для кожного завдання з його унікальним ID
        keyboard.append([InlineKeyboardButton(f"✅ Виконано: {task_text}", callback_data=str(task_id))])

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Твої завдання:", reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.message.chat_id
    task_id = int(query.data)

    # Видаляємо завдання з бази і змінюємо текст повідомлення
    delete_task(user_id, task_id)
    await query.edit_message_text(text="Завдання виконано і видалено!")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("tasks", show_tasks))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.add_handler(CallbackQueryHandler(button_handler))

app.run_polling()