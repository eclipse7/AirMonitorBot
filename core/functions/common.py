import logging

from telegram import Update, Bot, ParseMode

from core.functions.reply_markup import generate_user_markup, generate_hour_markup
from core.texts import *
from core.utils import send_async

LOGGER = logging.getLogger(__name__)


def error(bot: Bot, update, error, **kwargs):
    """ Error handling """
    LOGGER.error("An error (%s) occurred: %s"
                 % (type(error), error.message))


def user_panel(bot: Bot, update: Update):
    if update.message.chat.type == 'private':
        send_async(bot, chat_id=update.message.chat.id, text=MSG_START_WELCOME, parse_mode=ParseMode.HTML,
                   reply_markup=generate_user_markup())


def hour_panel(bot: Bot, update: Update, text):
    if update.message.chat.type == 'private':
        send_async(bot, chat_id=update.message.chat.id, text=text, reply_markup=generate_hour_markup())
