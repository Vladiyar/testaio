# -*- coding: utf-8 -*-
"""
Created on Mon Aug 17 09:30:22 2020

@author: vladi
"""

import asyncio
# import config
import logging
import requests
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import CallbackQuery
from sqlighter import SQLighter
from datetime import date


logging.basicConfig(level=logging.INFO)

# initialising bot
bot = Bot(token="1155158545:AAF-Z3nxdsxIkLT1Bl3LJrDZVRvTu2fmXiM")
dp = Dispatcher(bot)
db = SQLighter('privat_curr.db')


date = str(date.today())
id = 382233106


# money
keys = ['ccy', 'buy', 'sale']
USD, EUR, RUB, BTC = [], [], [], []
USD_old, EUR_old, RUB_old, BTC_old = [], [], [], []


# USD
data = requests.get('https://api.privatbank.ua/p24api/pubinfo?exchange&json&coursid=11').json()
for key in keys:
    USD.append(data[0].get(key))
# EUR
for key in keys:
    EUR.append(data[1].get(key))
# RUB
for key in keys:
    RUB.append(data[2].get(key))
# BTC
for key in keys:
    BTC.append(data[3].get(key))

USD_old = USD.copy()
EUR_old = EUR.copy()
RUB_old = RUB.copy()
BTC_old = BTC.copy()

# # USD_old
# for key in keys:
#     USD_old.append(data[0].get(key))
# # EUR
# for key in keys:
#     EUR_old.append(data[1].get(key))
# # RUB
# for key in keys:
#     RUB_old.append(data[2].get(key))
# # BTC
# for key in keys:
#     BTC_old.append(data[3].get(key))


USD_old[2] = str(db.get_usd())
EUR_old[2] = str(db.get_eur())
RUB_old[2] = str(db.get_rub())
BTC_old[2] = str(db.get_btc())


data_bel = requests.get('https://www.nbrb.by/api/exrates/rates?periodicity=0').json()
BEL = ['БЕЛАРУЦКИЙ РУБАЛЬ', str(data_bel[2].get('Cur_OfficialRate'))]

curr = '\n'.join(USD + EUR + RUB + BTC + BEL)
curr_2 =   USD_old[0] + '   ----------   ' + USD[0] + '\n' \
         + USD_old[1] + '   =>   ' + USD[1] + '\n' \
         + USD_old[2] + '   =>   ' + USD[2] + '\n' \
         + EUR_old[0] + '   ----------   ' + EUR[0] + '\n' \
         + EUR_old[1] + '   =>   ' + EUR[1] + '\n' \
         + EUR_old[2] + '   =>   ' + EUR[2] + '\n' \
         + RUB_old[0] + '   ----------   ' + RUB[0] + '\n' \
         + RUB_old[1] + '   =>   ' + RUB[1] + '\n' \
         + RUB_old[2] + '   =>   ' + RUB[2] + '\n' \
         + BTC_old[0] + '   ----------   ' + BTC[0] + '\n' \
         + BTC_old[1] + '   =>   ' + BTC[1] + '\n' \
         + BTC_old[2] + '   =>   ' + BTC[2]


async def checking(user_id):
    check = requests.get('https://api.privatbank.ua/p24api/pubinfo?exchange&json&coursid=11').json()
    for key in keys:
        USD.append(check[0].get(key))
    # EUR
    for key in keys:
        EUR.append(check[1].get(key))
    # RUB
    for key in keys:
        RUB.append(check[2].get(key))
    # BTC
    for key in keys:
        BTC.append(check[3].get(key))
    if not db.check_curr(USD[2]):
        db.set_curr(USD[2], EUR[2], RUB[2], BTC[2], date)
        await bot.send_message(user_id, curr_2)


@dp.message_handler(commands=['start'])
async def process_start(message: types.Message):
    await bot.send_message(message.from_user.id, 'Hello! Type /curr')
    print(USD)
    print(USD_old)
    print(curr_2)


@dp.message_handler(commands=['curr'])
async def process_start(message: types.Message):
    if db.check_curr(USD[2]):
        await bot.send_message(message.from_user.id, curr)
    else:
        await bot.send_message(message.from_user.id, curr_2)


async def periodic(sleep_for):
    while True:
        await asyncio.sleep(sleep_for)
        await checking(id)


if __name__ == "__main__":
    dp.loop.create_task(periodic(10))
    executor.start_polling(dp, skip_updates=True)
