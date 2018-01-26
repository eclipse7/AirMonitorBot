from telegram import ReplyKeyboardMarkup, KeyboardButton

from core.commands import *


def generate_user_markup():
    buttons = [[KeyboardButton(USER_COMMAND_DATA), KeyboardButton(USER_COMMAND_CO2)],
               [KeyboardButton(USER_COMMAND_TEMPERATURE), KeyboardButton(USER_COMMAND_HUMIDITY)]]
    return ReplyKeyboardMarkup(buttons, True)


def generate_hour_markup():
    buttons = [[KeyboardButton(USER_COMMAND_1_HOUR), KeyboardButton(USER_COMMAND_3_HOUR)],
               [KeyboardButton(USER_COMMAND_24_HOUR), KeyboardButton(USER_COMMAND_BACK)]]
    return ReplyKeyboardMarkup(buttons, True)
