import requests
from datetime import datetime
import logging
import asyncio
import config
from aiogram import Bot, Dispatcher, executor, types

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.API_TOKEN)
dp = Dispatcher(bot)

# subscription to bot
# @dp.message_handler(commands=['unsubscribe'])
# async def unsubscribe(message: types.Message):
#     if not db.subscriber_exists(message.from_user.id):
#         db.add_subscriber(message.from_user.id, False)
#         await message.answer("Вы и так не подписаны.")
#     else:
#         dp.update_subscription(message.from_user.id, False)
#         await message.answer("Вы успешно отписались от рассылки.")

keys = ['ccy', 'buy', 'sale']
USD, EUR, RUB, BTC = [], [], [], []
USDnow, EURnow, RUBnow, BTCnow = ['USD', '27.30000', '27.62431'], ['EUR', '1', '1'], ['RUB', '1', '1'], ['BTC', '1',
                                                                                                         '1']
user_id = 382233106


async def scheduler(wait_for):
    while True:
        await asyncio.sleep(wait_for)

        data = requests.get('https://api.privatbank.ua/p24api/pubinfo?exchange&json&coursid=11').json()
        # USD
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

        if "%.1f" % (float(USDnow[1])) != "%.1f" % (float(USD[1])):
            USDnow[1] = str(USD[1])
            USDnow[2] = USD[2]
            EURnow[1], EURnow[2], RUBnow[1], RUBnow[2], BTCnow[1], BTCnow[2] = EUR[1], EUR[2], RUB[1], RUB[2], BTC[
                1], BTC[2]
            curr = '\n'.join(USDnow + EURnow + RUBnow + BTCnow)

            # old tech p = requests.post(
            # f'https://api.telegram.org/bot1155158545:AAF-Z3nxdsxIkLT1Bl3LJrDZVRvTu2fmXiM/sendMessage?chat_id
            # =382233106&text={curr}')

            await bot.send_message(user_id, f"{curr}")


if __name__ == '__main__':
    dp.loop.create_task(scheduler(600))
    executor.start_polling(dp, skip_updates=True)
