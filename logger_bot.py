import logging

from environs import Env
import telegram


logger = logging.getLogger('Logger')
env = Env()
env.read_env()


class TelegramLogsHandler(logging.Handler):

    def __init__(self):
        super().__init__()
        self.chat_id = env.str('TG_CHAT_ID')
        self.tg_bot = telegram.Bot(token=env.str('TG_LOGGER_BOT_TOKEN'))

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)