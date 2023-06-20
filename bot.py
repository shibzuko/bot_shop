import logging
import datetime

from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

from test import add_user, get_user_id
from config import TOKEN








logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands='start')
async def start(message: types.Message):
    telegram_id = message.chat.id
    user_name = message.chat.username
    full_name = message.chat.full_name
    text_message = message.text
    date = message.date

    await message.answer(f'Салам алейкум\n\n{message}\n\n{type(message.date)}')


    if get_user_id(telegram_id) is None:  # Проверка наличия пользователя в БД
        add_user(telegram_id, user_name, full_name, date)
        print('dsssdsdd')










if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)