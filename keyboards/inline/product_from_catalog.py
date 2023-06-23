from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

#TODO: разобраться для чего тут  База данных
from loader import session

product_cb = CallbackData('product', 'id', 'action')


#TODO: может тут указать айди и цену?
def product_markup(idx='', price=3):

    global product_cb

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(f'Добавить в корзину - {price}₽', callback_data=product_cb.new(id=idx, action='add')))

    return markup