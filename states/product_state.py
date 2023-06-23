from aiogram.dispatcher.filters.state import StatesGroup, State

class ProductState(StatesGroup):
    product_name = State()
    product = State()
    price = State()
    amount = State()

class CategoryState(StatesGroup):
    category_name = State()