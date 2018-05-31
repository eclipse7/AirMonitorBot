import os
from datetime import datetime, timedelta

import matplotlib.pyplot as plt
from sqlalchemy import func, tuple_
from telegram import Update, Bot

from core.functions.reply_markup import generate_hour_markup
from core.texts import PLOT_X_LABEL_TEMP, PLOT_Y_LABEL_TEMP, PLOT_X_LABEL_HUM, PLOT_Y_LABEL_HUM
from core.types import Device


def data(bot: Bot, update: Update, session):
    if update.message.chat.type == 'private':
        sub_query = session.query(Device.device_id, func.max(Device.date)).group_by(Device.device_id).subquery()
        data = session.query(Device).filter(tuple_(Device.device_id, Device.date).in_(sub_query)).first()
        if data and (datetime.now() - data.date) < timedelta(minutes=5):
            text = ''
            # text += 'Дата: ' + str(data.date) + '\n'
            text += '🌱 CO₂: ' + str(data.ppm) + ' ppm \n'
            text += '🌡 Температура: ' + str(data.temp) + ' C \n'
            text += '🌊 Влажность: ' + str(round(data.hum)) + ' % \n'
            bot.sendMessage(update.message.chat.id, text)
        else:
            bot.sendMessage(update.message.chat.id, 'No data')


def temp_statistic(bot: Bot, update: Update, session, hour=1):
    device_data = session.query(Device).filter(datetime.now() - timedelta(
                    minutes=hour*60) < Device.date).order_by(Device.date).all()

    if not device_data:
        bot.sendMessage(update.message.chat.id, 'No data')
        return

    plt.switch_backend('ps')
    plt.xlabel(PLOT_X_LABEL_TEMP)
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

    text = 'Temperature '
    if hour == 1:
        text += '1h'
    elif hour == 3:
        text += '3h'
    elif hour == 24:
        text += '24h'
    text += ': ' + str(y[-1]) + ' C'

    with open(filename, 'rb') as file:
        bot.sendPhoto(update.message.chat.id, file, text, reply_markup=generate_hour_markup())
    plt.clf()
    os.remove(filename)


def hum_statistic(bot: Bot, update: Update, session, hour=1):
    device_data = session.query(Device).filter(datetime.now() - timedelta(
                    minutes=hour*60) < Device.date).order_by(Device.date).all()

    if not device_data:
        bot.sendMessage(update.message.chat.id, 'No data')
        return

    plt.switch_backend('ps')
    plt.xlabel(PLOT_X_LABEL_HUM)
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

    text = 'Humidity '
    if hour == 1:
        text += '1h'
    elif hour == 3:
        text += '3h'
    elif hour == 24:
        text += '24h'
    text += ': ' + str(y[-1]) + ' %'

    with open(filename, 'rb') as file:
        bot.sendPhoto(update.message.chat.id, file, text, reply_markup=generate_hour_markup())
    plt.clf()
    os.remove(filename)


def co2_statistic(bot: Bot, update: Update, session, hour=1):
    device_data = session.query(Device).filter(datetime.now() - timedelta(
                    minutes=hour*60) < Device.date).order_by(Device.date).all()

    if not device_data:
        bot.sendMessage(update.message.chat.id, 'No data')
        return

    plt.switch_backend('ps')
    plt.xlabel(PLOT_X_LABEL_HUM)
    plt.ylabel("CO2")
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

    text = 'CO₂ '
    if hour == 1:
        text += '1h'
    elif hour == 3:
        text += '3h'
    elif hour == 24:
        text += '24h'
    text += ': ' + str(y[-1]) + ' ppm'

    with open(filename, 'rb') as file:
        bot.sendPhoto(update.message.chat.id, file, text, reply_markup=generate_hour_markup())
    plt.clf()
    os.remove(filename)
