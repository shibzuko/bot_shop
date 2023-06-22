from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, ContentType, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.utils.callback_data import CallbackData
# from keyboards.default.markups import *
# from states import ProductState, CategoryState
from aiogram.types.chat import ChatActions
# from handlers.user.menu import settings
from loader import dp, bot, session, engine
from filters import IsAdmin
from hashlib import md5
from models import User, Messages, Product, Order, Order_items, Payment, Category

category_cb = CallbackData('category', 'id', 'action')
product_cb = CallbackData('product', 'id', 'action')

add_product = '➕ Добавить товар'
delete_category = '🗑️ Удалить категорию'

@dp.message_handler(IsAdmin(), commands='setting')
async def create_setting_keyboard(message: Message):
    markup = InlineKeyboardMarkup()
    request = session.query(Category).all()
    if len(request)>0:
        for id, category_name in request:
            markup.add(InlineKeyboardButton(
                category_name, callback_data=category_cb.new(id=id, action='view')))



