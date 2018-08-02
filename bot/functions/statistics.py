import os
from datetime import datetime, timedelta

import matplotlib.pyplot as plt
from sqlalchemy import func, tuple_
from telegram import Update, Bot
from telegram.ext.dispatcher import run_async

from bot.texts import PLOT_Y_LABEL_CO2, PLOT_Y_LABEL_HUM, PLOT_Y_LABEL_TEMP
from bot.types import Device


def data(bot: Bot, update: Update, session):
    if update.message.chat.type == 'private':
        sub_query = session.query(Device.device_id, func.max(Device.date)).group_by(Device.device_id).subquery()
        data = session.query(Device).filter(tuple_(Device.device_id, Device.date).in_(sub_query)).first()
        if data:
            text = ''
            if (datetime.now() - data.date) > timedelta(minutes=5):
                text += 'Дата: ' + str(data.date) + '\n'
            text += '🌱 CO₂: ' + str(data.ppm) + ' ppm \n'
            text += '🌡 Температура: ' + str(data.temp) + ' C \n'
            text += '🌊 Влажность: ' + str(round(data.hum)) + ' % \n'
            bot.sendMessage(update.message.chat.id, text)
        else:
            bot.sendMessage(update.message.chat.id, 'No data')


@run_async
def temp_statistic(bot: Bot, update: Update, session, hour=1):
    device_data = session.query(Device).filter(datetime.now() - timedelta(
                    minutes=hour*60) < Device.date).order_by(Device.date).all()

    if not device_data:
        bot.sendMessage(update.message.chat.id, 'No data')
        return

    plt.switch_backend('ps')
    plt.ylabel(PLOT_Y_LABEL_TEMP)
    x = [data.date for data in device_data]
    y = [data.temp for data in device_data]

    x.append(datetime.now())
    y.append(y[-1])
    plt.plot(x, y)

    ymin, ymax = plt.ylim()  # return the current ylim
    y_delta = ymax - ymin
    y_center = (ymax + ymin) / 2
    scale = 10
    if abs(y_delta) < scale:
        ymax = y_center + scale / 2
        ymin = y_center - scale / 2
    plt.ylim(ymin, ymax)

    plt.gcf().autofmt_xdate()
    filename = str(datetime.now()).replace(':', '').replace(' ', '').replace('-', '') + '.png'
    with open(filename, 'wb') as file:
        plt.savefig(file, format='png')

    text = str(hour) + 'h\n'
    text += 'Температура'
    text += ': ' + str(y[-1]) + ' C\n'
    text += '1 час: /temp_1\n'
    text += '3 часа: /temp_3\n'
    text += '24 часа: /temp_24\n'

    with open(filename, 'rb') as file:
        bot.sendPhoto(update.message.chat.id, file, text)
    plt.clf()
    os.remove(filename)


@run_async
def hum_statistic(bot: Bot, update: Update, session, hour=1):
    device_data = session.query(Device).filter(datetime.now() - timedelta(
                    minutes=hour*60) < Device.date).order_by(Device.date).all()

    if not device_data:
        bot.sendMessage(update.message.chat.id, 'No data')
        return

    plt.switch_backend('ps')
    plt.ylabel(PLOT_Y_LABEL_HUM)
    x = [data.date for data in device_data]
    y = [data.hum for data in device_data]

    x.append(datetime.now())
    y.append(y[-1])
    plt.plot(x, y)

    ymin, ymax = plt.ylim()  # return the current ylim
    y_delta = ymax - ymin
    y_center = (ymax + ymin) / 2
    scale = 40
    if abs(y_delta) < scale:
        ymax = y_center + scale / 2
        ymin = y_center - scale / 2
        if ymax > 105:
            ymax = 105
            ymin = ymax - scale
        if ymin < -5:
            ymin = -5
            ymax = ymin + scale
    plt.ylim(ymin, ymax)

    plt.gcf().autofmt_xdate()
    filename = str(datetime.now()).replace(':', '').replace(' ', '').replace('-', '') + '.png'
    with open(filename, 'wb') as file:
        plt.savefig(file, format='png')

    text = str(hour) + 'h\n'
    text += 'Влажность'
    text += ': ' + str(round(y[-1])) + ' %\n'
    text += '1 час: /hum_1\n'
    text += '3 часа: /hum_3\n'
    text += '24 часа: /hum_24\n'

    with open(filename, 'rb') as file:
        bot.sendPhoto(update.message.chat.id, file, text)
    plt.clf()
    os.remove(filename)


@run_async
def co2_statistic(bot: Bot, update: Update, session, hour=1):
    device_data = session.query(Device).filter(datetime.now() - timedelta(
                    minutes=hour*60) < Device.date).order_by(Device.date).all()

    if not device_data:
        bot.sendMessage(update.message.chat.id, 'No data')
        return

    plt.switch_backend('ps')
    plt.ylabel(PLOT_Y_LABEL_CO2)
    x = [data.date for data in device_data]
    y = [data.ppm for data in device_data]

    x.append(datetime.now())
    y.append(y[-1])
    plt.plot(x, y)

    ymin, ymax = plt.ylim()  # return the current ylim
    y_delta = ymax - ymin
    y_center = (ymax + ymin) / 2
    scale = 600
    if abs(y_delta) < scale:
        ymax = y_center + scale / 2
        ymin = y_center - scale / 2
        if ymax > 5000:
            ymax = 5000
            ymin = ymax - scale
        if ymin < 380:
            ymin = 380
            ymax = ymin + scale
    plt.ylim(ymin, ymax)

    plt.gcf().autofmt_xdate()
    filename = str(datetime.now()).replace(':', '').replace(' ', '').replace('-', '') + '.png'
    with open(filename, 'wb') as file:
        plt.savefig(file, format='png')

    text = str(hour) + 'h\n'
    text += 'CO₂'
    text += ': ' + str(y[-1]) + ' ppm \n'
    text += '1 час: /co2_1\n'
    text += '3 часа: /co2_3\n'
    text += '24 часа: /co2_24\n'

    with open(filename, 'rb') as file:
        bot.sendPhoto(update.message.chat.id, file, text)
    plt.clf()
    os.remove(filename)
