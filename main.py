import logging
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CallbackContext, CommandHandler, MessageHandler, filters, Application, ContextTypes
import json
import os

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def alarm(context: ContextTypes.DEFAULT_TYPE) -> None:
    job = context.job
    await context.bot.send_message(job.chat_id, text=job.data)


async def web_app_data(update: Update, context: CallbackContext) -> None:
    load = json.loads(update.message.web_app_data.data)
    chat_id = update.effective_message.chat_id
    context.job_queue.run_once(
        alarm, load["time"], chat_id=chat_id, name=str(chat_id), data=load["desc"])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kb = [
        [KeyboardButton("Create a new reminder", web_app=WebAppInfo(
            "https://dapizz01.github.io/ReminderBot_webui/"))]
    ]
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Insert a new reminder by using the keyboard that just popped up!", reply_markup=ReplyKeyboardMarkup(kb))


if __name__ == '__main__':
    TOKEN = os.environ["TOKEN"]

    application = ApplicationBuilder().token(TOKEN).build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    application.add_handler(MessageHandler(
        filters.StatusUpdate.WEB_APP_DATA, web_app_data))

    application.run_polling()
