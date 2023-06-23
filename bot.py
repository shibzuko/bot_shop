import logging
from aiogram import types
from aiogram.utils import executor
from utils.test import add_user, get_user_id, add_message
from loader import dp
import handlers


logging.basicConfig(level=logging.INFO)
# bot = Bot(token=TOKEN)
# dp = Dispatcher(bot)


@dp.message_handler(commands='start')
async def start(message: types.Message):
    telegram_id = message.chat.id
    user_name = message.chat.username
    full_name = message.chat.full_name
    text_message = message.text
    date = message.date



    await message.answer(f'Салам алейкум\n\n{message}')

    if get_user_id(telegram_id) is None:  # Проверка наличия пользователя в БД
        add_user(telegram_id, user_name, full_name, date)
        print('dsssdsdd')

    add_message(message)  # Adding a new message to the DB


@dp.message_handler(commands='add_new_product')
async def add_new_product(message: types.Message):
    await message.answer(f'Введите название наименование продукта')

@dp.message_handler()
async def random_message(message: types.Message):
    await message.answer(f'рандом')
    telegram_id = message.chat.id
    date = message.date
    text_message = message.text

    add_message(message)






if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)