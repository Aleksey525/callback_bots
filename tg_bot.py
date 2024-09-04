import logging
import time

import telegram
from environs import Env
from google.cloud import dialogflow
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from logs_handler import TelegramLogsHandler, logger


ERROR_CHECKING_DELAY = 10


def detect_intent_text(project_id, session_id, text, language_code='ru-RUS'):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    return response.query_result.fulfillment_text


def start(update: Update, context: CallbackContext):
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def echo_dialogflow(update: Update, context: CallbackContext):
    text = update.message.text
    project_id = context.bot_data['project_id']
    session_id = update.effective_chat.id
    df_response = detect_intent_text(project_id, session_id, text)
    update.message.reply_text(df_response)


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
            dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo_dialogflow))
            dispatcher.bot_data['project_id'] = project_id
            updater.start_polling()
            updater.idle()
        except Exception:
            logger.exception('Телеграм-бот упал с ошибкой:')
            time.sleep(ERROR_CHECKING_DELAY)


if __name__ == '__main__':
    main()
