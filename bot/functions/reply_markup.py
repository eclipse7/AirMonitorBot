from telegram import ReplyKeyboardMarkup, KeyboardButton

from bot.commands import *


def generate_user_markup():
    buttons = [
        [KeyboardButton(USER_COMMAND_DATA)],
        [KeyboardButton(USER_COMMAND_CO2), KeyboardButton(USER_COMMAND_TEMPERATURE)],
        [KeyboardButton(USER_COMMAND_PRESSURE), KeyboardButton(USER_COMMAND_HUMIDITY)]
    ]
    return ReplyKeyboardMarkup(buttons, True)
