from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

# buttons
cancel_button = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton("Cancel"))
start_button = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton("/start"))
result = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton("Get Visit Card"))
