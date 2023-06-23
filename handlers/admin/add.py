from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, ContentType, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.utils.callback_data import CallbackData
from keyboards.default.markup import *
from states import ProductState, CategoryState
from aiogram.types.chat import ChatActions
# from handlers.user.menu import settings
from loader import dp, bot, session, engine, delete
from filters import IsAdmin
from hashlib import md5
from models import User, Messages, Product, Order, Order_items, Payment, Category
import handlers
import keyboards


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




@dp.message_handler(IsAdmin(), commands='delete_category')
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









#TODO: #################################################################
# add product


@dp.message_handler(IsAdmin(), text=add_product)
async def process_add_product(message: Message):
    await ProductState.product_name.set()

    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(cancel_message)

    await message.answer('Название?', reply_markup=markup)


# "Отменить действие" или Завершение состояния и возврат к категориям
@dp.message_handler(IsAdmin(), text=cancel_message, state=ProductState.product_name)
async def process_cancel(message: Message, state: FSMContext):
    await message.answer('Действие отменено!', reply_markup=ReplyKeyboardRemove())
    await state.finish()

    await create_setting_keyboard(message)


# "Назад" или возвращает в категории с сохранением состояния
@dp.message_handler(IsAdmin(), text=back_message, state=ProductState.product_name)
async def process_title_back(message: Message, state: FSMContext):
    await process_add_product(message)


@dp.message_handler(IsAdmin(), state=ProductState.product_name)
async def process_title(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['product_name'] = message.text

    await ProductState.next()
    await message.answer('Введите цифровой продукт (Ключ🔑)', reply_markup=back_markup())


@dp.message_handler(IsAdmin(), text=back_message, state=ProductState.body)
async def process_body_back(message: Message, state: FSMContext):
    await ProductState.product_name.set()

    async with state.proxy() as data:
        await message.answer(f"Изменить название с <b>{data['product_name']}</b>?", reply_markup=back_markup())


@dp.message_handler(IsAdmin(), state=ProductState.body)
async def process_body(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['body'] = message.text

    await ProductState.next()
    await message.answer('Фото?', reply_markup=back_markup())


@dp.message_handler(IsAdmin(), content_types=ContentType.PHOTO, state=ProductState.image)
async def process_image_photo(message: Message, state: FSMContext):
    fileID = message.photo[-1].file_id
    file_info = await bot.get_file(fileID)
    downloaded_file = (await bot.download_file(file_info.file_path)).read()

    async with state.proxy() as data:
        data['image'] = downloaded_file

    await ProductState.next()
    await message.answer('Цена?', reply_markup=back_markup())


@dp.message_handler(IsAdmin(), content_types=ContentType.TEXT, state=ProductState.image)
async def process_image_url(message: Message, state: FSMContext):
    if message.text == back_message:

        await ProductState.body.set()

        async with state.proxy() as data:

            await message.answer(f"Изменить описание с <b>{data['body']}</b>?", reply_markup=back_markup())

    else:

        await message.answer('Вам нужно прислать фото товара.')


@dp.message_handler(IsAdmin(), lambda message: not message.text.isdigit(), state=ProductState.price)
async def process_price_invalid(message: Message, state: FSMContext):
    if message.text == back_message:

        await ProductState.image.set()

        async with state.proxy() as data:

            await message.answer("Другое изображение?", reply_markup=back_markup())

    else:

        await message.answer('Укажите цену в виде числа!')


@dp.message_handler(IsAdmin(), lambda message: message.text.isdigit(), state=ProductState.price)
async def process_price(message: Message, state: FSMContext):


@dp.message_handler(IsAdmin(), lambda message: message.text not in [back_message, all_right_message],
                    state=ProductState.confirm)
async def process_confirm_invalid(message: Message, state: FSMContext):
    await message.answer('Такого варианта не было.')


@dp.message_handler(IsAdmin(), text=back_message, state=ProductState.confirm)
async def process_confirm_back(message: Message, state: FSMContext):
    await ProductState.price.set()

    async with state.proxy() as data:
        await message.answer(f"Изменить цену с <b>{data['price']}</b>?", reply_markup=back_markup())















# @dp.message_handler(IsAdmin(), text=all_right_message, state=ProductState.confirm)
# async def process_confirm(message: Message, state: FSMContext):
#     async with state.proxy() as data:
#         product_name = data['product_name']
#         body = data['body']
#         image = data['image']
#         price = data['price']
#
#         tag = db.fetchone(
#             'SELECT title FROM categories WHERE idx=?', (data['category_index'],))[0]
#         idx = md5(' '.join([title, body, price, tag]
#                            ).encode('utf-8')).hexdigest()
#
#         db.query('INSERT INTO products VALUES (?, ?, ?, ?, ?, ?)',
#                  (idx, title, body, image, int(price), tag))
#
#     await state.finish()
#     await message.answer('Готово!', reply_markup=ReplyKeyboardRemove())
#     await create_setting_keyboard(message)
#
#
# # delete product
#
#
# @dp.callback_query_handler(IsAdmin(), product_cb.filter(action='delete'))
# async def delete_product_callback_handler(query: CallbackQuery, callback_data: dict):
#     product_idx = callback_data['id']
#     db.query('DELETE FROM products WHERE idx=?', (product_idx,))
#     await query.answer('Удалено!')
#     await query.message.delete()
#
#
# async def show_products(m, products, category_idx):
#     await bot.send_chat_action(m.chat.id, ChatActions.TYPING)
#
#     for idx, title, body, image, price, tag in products:
#         text = f'<b>{title}</b>\n\n{body}\n\nЦена: {price} рублей.'
#
#         markup = InlineKeyboardMarkup()
#         markup.add(InlineKeyboardButton(
#             '🗑️ Удалить', callback_data=product_cb.new(id=idx, action='delete')))
#
#         await m.answer_photo(photo=image,
#                              caption=text,
#                              reply_markup=markup)
#
#     markup = ReplyKeyboardMarkup()
#     markup.add(add_product)
#     markup.add(delete_category)
#
#     await m.answer('Хотите что-нибудь добавить или удалить?', reply_markup=markup)

