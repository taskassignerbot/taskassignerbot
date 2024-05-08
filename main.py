from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, CallbackContext, ContextTypes, filters, Application
import logging
from typing import Final
from text_extractor import process_voice_file_and_get_text

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN: Final=get_telegram_api_key()

employees = {
    "полина" : 642887648,
    "глеб" : 763447170,
    "света" : 1340252477,
    "polina" : 642887648,
    "gleb" : 763447170,
    "sveta" : 1340252477
}

def message_is_correct(text):
    # Simple implementation
    return text.startswith("Сообщи ")

def extract_name(text):
    words = text.lower().split(' ')
    _, rest = text.split("Сообщи ", 1)
    name = rest.split(", что", 1)[0]
    return name

def extract_message(text):
    # Simple implementation
    _, rest = text.split("Сообщи ", 1)
    message = rest.split(", что", 1)[1]
    return message

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

async def send_message(bot, chat_id, message):
    await bot.send_message(chat_id=chat_id, text=message)

async def handle_text_message(update: Update, context: CallbackContext) -> None:
    text = update.message.text
    employee_id = update.message.chat.id
    print(employee_id)
    if message_is_correct(text):
        try:
            name = extract_name(text)
            message = extract_message(text)
            if name in employees:
                employee_chat_id = employees[name]
                await send_message(context.bot, employee_chat_id, message)
                await update.message.reply_text(f'Сообщение для {name} отправлено.')
            else:
                await update.message.reply_text('Имя сотрудника не найдено.')
        except ValueError:
            await update.message.reply_text('Неверный формат сообщения.')
    else:
        await update.message.reply_text('Пожалуйста, используйте формат "Сообщи [имя], что [сообщение]".')

async def handle_audio_message(update: Update, context: CallbackContext) -> None:
    voice_file = await update.message.voice.get_file()
    text =  await process_voice_file_and_get_text(voice_file)
    
    await update.message.reply_text(text=text)
    await update.message.reply_text('=====')


def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_message))
    application.add_handler(MessageHandler(filters.VOICE, handle_audio_message))
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
