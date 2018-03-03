# -*- coding: utf-8 -*-

import logging

from telegram import (
    Bot, Update
)
from telegram.ext import (
    Updater, CommandHandler, MessageHandler,
    Filters
)
from telegram.ext.dispatcher import run_async

from config import TOKEN
from core.commands import *
from core.functions.common import (
    ping, user_panel, error
)
from core.functions.statistics import data, temp_statistic, hum_statistic, co2_statistic
from core.types import user_allowed

logging.basicConfig(
    level=logging.WARNING,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


# Without @run_async
@user_allowed
def manage_all(bot: Bot, update: Update, session, chat_data: dict):
    if update.message.chat.type == 'private':
        if not update.message.text:
            return

        text = update.message.text
        if update.message.text:
            if text == USER_COMMAND_DATA:
                data(bot, update, session)

            elif text == USER_COMMAND_CO2:
                chat_data['mode'] = 'co2'
                co2_statistic(bot, update, session, hour=1)

            elif text == USER_COMMAND_TEMPERATURE:
                chat_data['mode'] = 'temp'
                temp_statistic(bot, update, session, hour=1)

            elif text == USER_COMMAND_HUMIDITY:
                chat_data['mode'] = 'hum'
                hum_statistic(bot, update, session, hour=1)

            elif text == USER_COMMAND_1_HOUR:
                mode = chat_data['mode']
                if mode == 'co2':
                    co2_statistic(bot, update, session, hour=1)
                elif mode == 'temp':
                    temp_statistic(bot, update, session, hour=1)
                elif mode == 'hum':
                    hum_statistic(bot, update, session, hour=1)

            elif text == USER_COMMAND_3_HOUR:
                mode = chat_data['mode']
                if mode == 'co2':
                    co2_statistic(bot, update, session, hour=3)
                elif mode == 'temp':
                    temp_statistic(bot, update, session, hour=3)
                elif mode == 'hum':
                    hum_statistic(bot, update, session, hour=3)

            elif text == USER_COMMAND_24_HOUR:
                mode = chat_data['mode']
                if mode == 'co2':
                    co2_statistic(bot, update, session, hour=24)
                elif mode == 'temp':
                    temp_statistic(bot, update, session, hour=24)
                elif mode == 'hum':
                    hum_statistic(bot, update, session, hour=24)

            else:
                user_panel(bot, update)
                chat_data['mode'] = ''


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    disp = updater.dispatcher

    # on different commands - answer in Telegram
    disp.add_handler(CommandHandler('start', user_panel))
    disp.add_handler(CommandHandler('ping', ping))
    disp.add_handler(MessageHandler(
        Filters.all, manage_all, pass_chat_data=True))

    # log all errors
    disp.add_error_handler(error)

    # Start the Bot
    updater.start_polling(poll_interval=1)
    # app.run(port=API_PORT)
    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
