"""
Base of notification system
"""
from datetime import datetime

import telepot

from lifeguard.logger import lifeguard_logger as logger
from lifeguard.notifications import NotificationBase

from lifeguard_telegram.settings import (
    TELEGRAM_API_KEY,
    TELEGRAM_DEFAULT_CHAT_ID,
)

HEADERS = {"Content-Type": "application/json; charset=UTF-8"}


class TelegramNotificationBase(NotificationBase):
    """
    Telegram notification
    """

    @property
    def name(self):
        return "telegram"

    def send_single_message(self, content, settings):
        logger.info("seding single message to msteams")

        self.__send_message(content, settings)

    def init_thread(self, content, settings):
        logger.info("notify a new problem")

        self.__send_message(content, settings)

        return [datetime.now().strftime("%Y%m%d%H%M")]

    def update_thread(self, threads, content, settings):
        logger.info("notify updating problem status %s", threads)
        self.__send_message(content, settings)

    def close_thread(self, threads, content, settings):
        logger.info("notify closing problem status %s", threads)
        self.__send_message(content, settings)

    def __send_message(self, content, settings):
        if not isinstance(content, list):
            content = [content]

        for chat in (
            settings.get("notification", {})
            .get("telegram", {})
            .get("chats", [TELEGRAM_DEFAULT_CHAT_ID])
        ):
            for entry in content:
                self.__call_bot_send_message(chat, entry)

    def __call_bot_send_message(self, chat, text):
        logger.info("sending message to chat %s", chat)
        try:
            self.__get_bot().sendMessage(chat, text=text, parse_mode="Markdown")
        except Exception as error:
            logger.error("error sending message to chat %s", chat)
            logger.error(error)
            self.__get_bot().sendMessage(
                chat, text="there was an error sending the message"
            )

    def __get_bot(self):
        if not hasattr(self, "__bot"):
            self.__bot = telepot.Bot(TELEGRAM_API_KEY)
        return self.__bot
