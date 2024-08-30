import logging
import random
import time

from google.cloud import dialogflow
from environs import Env
import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType

from logger_bot import TelegramLogsHandler


ERROR_CHECKING_DELAY = 10

logger = logging.getLogger('Logger')


def detect_intent_text(project_id, session_id, text, language_code='ru-RUS'):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    if response.query_result.intent.is_fallback:
        return None
    else:
        return response.query_result.fulfillment_text


def echo(event, vk_api, message):
    vk_api.messages.send(
        user_id=event.user_id,
        message=message,
        random_id=random.randint(1,1000)
    )


def main():
    env = Env()
    env.read_env()
    bot_token = env.str('VK_BOT_TOKEN')
    project_id = env.str('PROJECT_ID')
    vk_session = vk.VkApi(token=bot_token)
    vk_api = vk_session.get_api()
    logger.setLevel(logging.DEBUG)
    telegram_handler = TelegramLogsHandler()
    telegram_handler.setLevel(logging.DEBUG)
    logger.addHandler(telegram_handler)
    logger.info('VK-бот запущен')
    while True:
        try:
            longpoll = VkLongPoll(vk_session)
            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    user_message = event.text
                    response_df = detect_intent_text(project_id, event.user_id, user_message)
                    if response_df:
                        echo(event, vk_api, response_df)
        except Exception:
            logger.exception('Бот упал с ошибкой:')
            time.sleep(ERROR_CHECKING_DELAY)


if __name__ == '__main__':
    main()