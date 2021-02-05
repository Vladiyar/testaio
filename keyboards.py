from aiogram.types import ReplyKeyboardMarkup, \
                          KeyboardButton

btnHello = KeyboardButton("Hello!")
greet_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(btnHello)

btnUp = KeyboardButton("Update!")
up_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(btnUp)