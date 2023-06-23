from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from loader import session
from models import Category

category_cb = CallbackData('category', 'id', 'action')


def categories_markup():
    global category_cb

    markup = InlineKeyboardMarkup()
    result = session.query(Category).all()
    for id, categoru_name in result:
        markup.add(InlineKeyboardButton(categoru_name, callback_data=category_cb.new(id=id, action='view')))

    return markup
