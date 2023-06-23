from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, ContentType, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.utils.callback_data import CallbackData
# from keyboards.default.markups import *
from states import ProductState, CategoryState
from aiogram.types.chat import ChatActions
# from handlers.user.menu import settings
from loader import dp, bot, session, engine, delete
from filters import IsAdmin
from hashlib import md5
from models import User, Messages, Product, Order, Order_items, Payment, Category
import handlers


category_cb = CallbackData('category', 'id', 'action')
product_cb = CallbackData('product', 'id', 'action')

add_product = "➕ Добавить товар"
delete_category = "🗑️ Удалить категорию"



#  Формирование и вывод клавиатуры состоящей из списка категорий из БД + кнопка добавления новой категории
@dp.message_handler(IsAdmin(), commands='setting')
async def create_setting_keyboard(message: Message):
    markup = InlineKeyboardMarkup()
    request = session.query(Category).all()
    if len(request)>0:
        for category in request:
            markup.add(InlineKeyboardButton(
                category.category_name, callback_data=category_cb.new(id=category.id, action='view')))

    markup.add(InlineKeyboardButton(
        "➕ Добавить категорию",callback_data='add_category'))
    await message.answer("⚙️ Настройки категорий:", reply_markup=markup)



# Обратный вызов при нажатии на существующую категорию
@dp.callback_query_handler(IsAdmin(), category_cb.filter(action='view'))
async def category_callback_handler(query: CallbackQuery, callback_data: dict, state: FSMContext):
    category_id = callback_data['id']
    products_from_category = session.query(Product).filter_by(category_id=category_id)
    await query.message.delete()
    await query.answer('Все товары этой категории:')
    await query.message.answer('Все товары этой категории:')
    await state.update_data(category_index=category_id)  # Обновляет данные состояния (FSMContext) для данного пользователя
    # await show_products(query.message, products_from_category, category_id)



# Добавление новой категории add_category
@dp.callback_query_handler(IsAdmin(), text='add_category')
async def add_category_callback_handler(query: CallbackQuery):
    await query.message.delete()
    await query.message.answer("Введите название категории:")
    await CategoryState.category_name.set()  # Устанавливает состояние CategoryState.title для пользователя с помощью



@dp.message_handler(IsAdmin(), state=CategoryState.category_name)
async def set_category_title(message: Message, state: FSMContext):
    category_title = message.text
    add_category_title = Category(
        category_name = category_title
    )
    session.merge(add_category_title)
    session.commit()
    await state.finish()  # Завершает состояние CategoryState
    await create_setting_keyboard(message)  # Формирование и вывод клавиатуры




@dp.message_handler(IsAdmin(), text=delete_category)
async def delede_category_handler(message: Message, state: FSMContext):

    async with state.proxy() as data:
        if 'category_index' in data.keys():

            index = data['category_index']

            # Удаление товаров связанных с категорией
            session.execute(delete(Product).where(
                Product.category_id == session.query(Category.id).filter(Category.id == index)))

            # Удаление категории
            session.execute(delete(Category).where(Category.id == index))

            session.commit()



