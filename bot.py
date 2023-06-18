import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from config import TOKEN








logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands='start')
async def start(message: types.Message):
    chat_id = message.chat.id
    await message.answer(f'Салам алейкум')






if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)