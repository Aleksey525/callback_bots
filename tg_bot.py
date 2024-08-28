import logging

from environs import Env
from google.cloud import dialogflow
import telegram
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext


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
    f = detect_intent_text(project_id, session_id, text)
    update.message.reply_text(f)


def main():
    env = Env()
    env.read_env()
    bot_token = env.str('TG_BOT_TOKEN')
    project_id = env.str('PROJECT_ID')
    updater = Updater(bot_token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo_dialogflow))
    dispatcher.bot_data['project_id'] = project_id
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
