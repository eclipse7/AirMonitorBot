from telegram import Bot
from telegram.error import TelegramError
from telegram.ext.dispatcher import run_async


@run_async
def send_async(bot: Bot, *args, **kwargs):
    try:
        return bot.sendMessage(*args, **kwargs)

    except TelegramError:
        return None
