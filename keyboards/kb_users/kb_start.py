from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

kb_start = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

button1 = KeyboardButton(text='/подписки')
button2 = KeyboardButton(text='/панель_администратора')
button3 = KeyboardButton(text='/помощь')

kb_start.row(button1, button2, button3)
