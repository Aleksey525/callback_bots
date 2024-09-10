import logging
import random
import time

from environs import Env
import telegram
import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType

from google_df_api import detect_intent_text
from logs_handler import TelegramLogsHandler, logger


ERROR_CHECKING_DELAY = 10


def get_response_df(event, vk_api, message):
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
    chat_id = env.str('TG_CHAT_ID')
    logger_bot = telegram.Bot(token=env.str('TG_LOGGER_BOT_TOKEN'))
    vk_api = vk_session.get_api()
    logger.setLevel(logging.DEBUG)
    telegram_handler = TelegramLogsHandler(chat_id, logger_bot)
    telegram_handler.setLevel(logging.DEBUG)
    logger.addHandler(telegram_handler)
    logger.info('VK-бот запущен')
    while True:
        try:
            longpoll = VkLongPoll(vk_session)
            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    user_message = event.text
                    df_response_text, df_response_status = detect_intent_text(project_id, event.user_id, user_message)
                    if not df_response_status:
                        get_response_df(event, vk_api, df_response_text)
        except Exception:
            logger.exception('VK-бот упал с ошибкой:')
            time.sleep(ERROR_CHECKING_DELAY)


if __name__ == '__main__':
    main()