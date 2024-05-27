from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CommandHandler, MessageHandler, CallbackContext, ContextTypes, filters, Application
import logging
from typing import Final
import json
from text_extractor import process_voice_file_and_get_text, paraphrase_message
from functions import extract_name, define_adressee
from api_keys import get_telegram_api_key

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = get_telegram_api_key()

with open('employees.json', 'r') as json_file:
    employees = json.load(json_file)
employees_names = employees.keys()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

async def send_message(bot, chat_id, message):
    await bot.send_message(chat_id=chat_id, text=message)

async def handle_text_message(update: Update, context: CallbackContext) -> None:
    text = update.message.text
    print(update.message.chat.id)
    text_to_send = paraphrase_message(text)
    name = define_adressee(text_to_send.split()[0])
    if name:
        employee_chat_id = employees[name]
        await send_message(context.bot, employee_chat_id, text_to_send[1:-2])
    else:
        await update.message.reply_text(f'Имя {name} не найдено в списке сотрудников')
    pass


async def handle_audio_message(update: Update, context: CallbackContext) -> None:
    voice_file = await update.message.voice.get_file()
    print(update.message.chat.id)
    text =  await process_voice_file_and_get_text(voice_file)
    text_to_send = paraphrase_message(text)
    name = define_adressee(text_to_send.split()[0])
    print(text_to_send)
    if name:
        employee_chat_id = employees[name]
        await send_message(context.bot, employee_chat_id, text_to_send[1:-2])
    else:
        await update.message.reply_text('Имя не найдено в списке сотрудников')


def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    # application.add_handler(CommandHandler("new_employee", add_new_employee))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_message))
    application.add_handler(MessageHandler(filters.VOICE, handle_audio_message))
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
