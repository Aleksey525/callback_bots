import logging
import time

import telegram
from environs import Env
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from google_df_api import detect_intent_text
from logs_handler import TelegramLogsHandler, logger


ERROR_CHECKING_DELAY = 10


def start(update: Update, context: CallbackContext):
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def get_response_df(update: Update, context: CallbackContext):
    text = update.message.text
    project_id = context.bot_data['project_id']
    session_id = update.effective_chat.id
    df_response_text, df_response_status = detect_intent_text(project_id, session_id, text)
    if df_response_text:
        update.message.reply_text(df_response_text)


def main():
    env = Env()
    env.read_env()
    bot_token = env.str('TG_BOT_TOKEN')
    project_id = env.str('PROJECT_ID')
    chat_id = env.str('TG_CHAT_ID')
    logger_bot = telegram.Bot(token=env.str('TG_LOGGER_BOT_TOKEN'))
    logger.setLevel(logging.DEBUG)
    telegram_handler = TelegramLogsHandler(chat_id, logger_bot)
    telegram_handler.setLevel(logging.DEBUG)
    logger.addHandler(telegram_handler)
    logger.info('Телеграм-бот запущен')
    updater = Updater(bot_token)
    while True:
        try:
            dispatcher = updater.dispatcher
            dispatcher.add_handler(CommandHandler("start", start))
            dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, get_response_df))
            dispatcher.bot_data['project_id'] = project_id
            updater.start_polling()
            updater.idle()
        except Exception:
            logger.exception('Телеграм-бот упал с ошибкой:')
            time.sleep(ERROR_CHECKING_DELAY)


if __name__ == '__main__':
    main()
