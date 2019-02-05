import os
from datetime import datetime, timedelta

import matplotlib.pyplot as plt
from telegram import Update, Bot
from telegram.ext.dispatcher import run_async

from bot.texts import PLOT_Y_LABEL_CO2, PLOT_Y_LABEL_HUM, PLOT_Y_LABEL_TEMP, PLOT_Y_LABEL_PRESSURE
from bot.types import collection


figsize = (8, 5.65)
# style = 'bmh'
style = 'seaborn-whitegrid'

@run_async
def data(bot: Bot, update: Update):
    if update.message.chat.type == 'private':
        device_data = collection.find().sort("date", -1)
        data = device_data[0]

        if data:
            text = ''
            if (datetime.now() - data['date']) > timedelta(minutes=5):
                text += 'Дата: ' + str(data['date']) + '\n'
            text += '🌱 CO₂: ' + str(data['ppm']) + ' ppm \n'
            text += '🌡 Температура #1: ' + str(data['temp']) + ' C \n'
            text += '🌡 Температура #2: ' + str(data['bmp180_temp']) + ' C \n'
            text += '🌊 Влажность: ' + str(round(data['hum'])) + ' % \n'
            text += '🏔 Aтм. Давление: ' + str(round(data['pressure'])) + ' mmHg \n'
            bot.sendMessage(update.message.chat.id, text)
        else:
            bot.sendMessage(update.message.chat.id, 'No data')


@run_async
def temp_statistic(bot: Bot, update: Update, hour=1):
    device_data = collection.find({'date': {'$gt': datetime.now() - timedelta(minutes=hour*60)}}).sort("date", 1)
    if not device_data:
        bot.sendMessage(update.message.chat.id, 'No data')
        return

    plt.style.use(style)
    plt.switch_backend('ps')
    plt.figure(figsize=figsize)
    plt.title(PLOT_Y_LABEL_TEMP)
    x = []
    y = []
    z = []
    for data in device_data:
        if data.get('bmp180_temp') and data.get('temp'):
            x.append(data['date'])
            y.append(data['temp'])
            z.append(data['bmp180_temp'])

    x.append(datetime.now())
    y.append(y[-1])
    z.append(z[-1])

    plt.plot(x, y)
    plt.plot(x, z)
    plt.grid(True)

    ymin, ymax = plt.ylim()  # return the current ylim
    y_delta = ymax - ymin
    y_center = (ymax + ymin) / 2
    scale = 10
    if abs(y_delta) < scale:
        ymax = y_center + scale / 2
        ymin = y_center - scale / 2
    plt.ylim(ymin, ymax)
    # plt.fill_between(x, ymin, y, alpha=0.7, interpolate=True)

    plt.gcf().autofmt_xdate()
    filename = str(datetime.now()).replace(':', '').replace(' ', '').replace('-', '') + '.png'
    with open(filename, 'wb') as file:
        plt.savefig(file, format='png')

    text = str(hour) + 'h\n'
    text += '🌡 Температура #1: '
    text += str(y[-1]) + ' C\n'
    text += '🌡 Температура #2: '
    text += str(z[-1]) + ' C\n'
    text += '1 час: /temp_1\n'
    text += '3 часа: /temp_3\n'
    text += '24 часа: /temp_24\n'

    with open(filename, 'rb') as file:
        bot.sendPhoto(update.message.chat.id, file, text)
    plt.clf()
    os.remove(filename)


@run_async
def hum_statistic(bot: Bot, update: Update, hour=1):
    device_data = collection.find({'date': {'$gt': datetime.now() - timedelta(minutes=hour * 60)}}).sort("date", 1)
    if not device_data:
        bot.sendMessage(update.message.chat.id, 'No data')
        return

    plt.style.use(style)
    plt.switch_backend('ps')
    plt.figure(figsize=figsize)
    plt.title(PLOT_Y_LABEL_HUM)
    x = []
    y = []
    for data in device_data:
        x.append(data['date'])
        y.append(data['hum'])

    x.append(datetime.now())
    y.append(y[-1])
    plt.plot(x, y)
    plt.grid(True)

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
    plt.fill_between(x, ymin, y, alpha=0.7, interpolate=True)

    plt.gcf().autofmt_xdate()
    filename = str(datetime.now()).replace(':', '').replace(' ', '').replace('-', '') + '.png'
    with open(filename, 'wb') as file:
        plt.savefig(file, format='png')

    text = str(hour) + 'h\n'
    text += '🌊 Влажность: '
    text += str(round(y[-1])) + ' %\n'
    text += '1 час: /hum_1\n'
    text += '3 часа: /hum_3\n'
    text += '24 часа: /hum_24\n'

    with open(filename, 'rb') as file:
        bot.sendPhoto(update.message.chat.id, file, text)
    plt.clf()
    os.remove(filename)


@run_async
def co2_statistic(bot: Bot, update: Update, hour=1):
    device_data = collection.find({'date': {'$gt': datetime.now() - timedelta(minutes=hour * 60)}}).sort("date", 1)
    if not device_data:
        bot.sendMessage(update.message.chat.id, 'No data')
        return

    plt.style.use(style)
    plt.switch_backend('ps')
    plt.figure(figsize=figsize)
    plt.title(PLOT_Y_LABEL_CO2)
    x = []
    y = []
    for data in device_data:
        x.append(data['date'])
        y.append(data['ppm'])

    x.append(datetime.now())
    y.append(y[-1])
    plt.plot(x, y)
    plt.grid(True)

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
    plt.fill_between(x, ymin, y, alpha=0.7, interpolate=True)

    plt.gcf().autofmt_xdate()
    filename = str(datetime.now()).replace(':', '').replace(' ', '').replace('-', '') + '.png'
    with open(filename, 'wb') as file:
        plt.savefig(file, format='png')

    text = str(hour) + 'h\n'
    text += '🌱 CO₂: '
    text += str(y[-1]) + ' ppm \n'
    text += '1 час: /co2_1\n'
    text += '3 часа: /co2_3\n'
    text += '24 часа: /co2_24\n'

    with open(filename, 'rb') as file:
        bot.sendPhoto(update.message.chat.id, file, text)
    plt.clf()
    os.remove(filename)


@run_async
def pressure_statistic(bot: Bot, update: Update, hour=1):
    device_data = collection.find({'date': {'$gt': datetime.now() - timedelta(minutes=hour * 60)}}).sort("date", 1)
    if not device_data:
        bot.sendMessage(update.message.chat.id, 'No data')
        return

    plt.style.use(style)
    plt.switch_backend('ps')
    plt.figure(figsize=figsize)
    plt.title(PLOT_Y_LABEL_PRESSURE)
    x = []
    y = []
    for data in device_data:
        if data.get('pressure'):
            x.append(data['date'])
            y.append(data['pressure'])

    x.append(datetime.now())
    y.append(y[-1])
    plt.plot(x, y)
    plt.grid(True)

    ymin, ymax = plt.ylim()  # return the current ylim
    y_delta = ymax - ymin
    y_center = (ymax + ymin) / 2
    scale = 20
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
    plt.fill_between(x, ymin, y, alpha=0.7, interpolate=True)

    plt.gcf().autofmt_xdate()
    filename = str(datetime.now()).replace(':', '').replace(' ', '').replace('-', '') + '.png'
    with open(filename, 'wb') as file:
        plt.savefig(file, format='png')

    text = str(hour) + 'h\n'
    text += '🏔 Aтм. Давление: '
    text += str(round(y[-1])) + ' mmHg \n'
    text += '1 час: /p_1\n'
    text += '3 часа: /p_3\n'
    text += '24 часа: /p_24\n'

    with open(filename, 'rb') as file:
        bot.sendPhoto(update.message.chat.id, file, text)
    plt.clf()
    os.remove(filename)
