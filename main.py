import logging
import time

from telegram import (
    Bot, Update
)
from telegram.ext import (
    Updater, CommandHandler, MessageHandler,
    Filters
)

from bot.commands import *
from bot.functions.common import (
    ping, user_panel, error
)
from bot.functions.statistics import data, temp_statistic, hum_statistic, co2_statistic
from config import TOKEN, IP, PORT
from web_app import app

logging.basicConfig(
    level=logging.WARNING,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


def manage_all(bot: Bot, update: Update, chat_data: dict):
    if update.message.chat.type == 'private':
        text = update.message.text
        if not text:
            return

        # Avoid flood
        now = time.time()
        if ((now - chat_data.get('last_time', 0)) < 1.1) and (chat_data.get('last_text', None) == text) or \
                ((now - chat_data.get('last_time', 0)) < 0.2):
            chat_data['last_text'] = text
            chat_data['last_time'] = now
            return
        chat_data['last_time'] = now
        chat_data['last_text'] = text

        if text == USER_COMMAND_DATA:
            data(bot, update)

        elif text == USER_COMMAND_CO2:
            co2_statistic(bot, update, hour=1)

        elif text == USER_COMMAND_TEMPERATURE:
            temp_statistic(bot, update, hour=1)

        elif text == USER_COMMAND_HUMIDITY:
            hum_statistic(bot, update, hour=1)

        elif text.startswith('/co2'):
            arg = int(text.split('_')[1])
            if arg:
                co2_statistic(bot, update, hour=arg)

        elif text.startswith('/temp'):
            arg = int(text.split('_')[1])
            if arg:
                temp_statistic(bot, update, hour=arg)

        elif text.startswith('/hum'):
            arg = int(text.split('_')[1])
            if arg:
                hum_statistic(bot, update, hour=arg)

        else:
            user_panel(bot, update)


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    disp = updater.dispatcher

    # on different commands - answer in Telegram
    disp.add_handler(CommandHandler('start', user_panel))
    disp.add_handler(CommandHandler('help', user_panel))
    disp.add_handler(CommandHandler('ping', ping))
    disp.add_handler(MessageHandler(
        Filters.all, manage_all, pass_chat_data=True))

    # log all errors
    disp.add_error_handler(error)

    # Start the Bot
    print('Start bot')
    # updater.start_polling(poll_interval=1)
    updater.start_webhook(listen='0.0.0.0',
                          port=PORT,
                          url_path=TOKEN,
                          key='private.key',
                          cert='cert.pem',
                          webhook_url='https://%s:%s/%s' % (IP, PORT, TOKEN))

    # Create Web server, receive data from sensor (blocking function)
    print('Start web server')
    app.run(debug=False, host='0.0.0.0', port=1883)

    # updater.idle()


if __name__ == '__main__':
    main()
