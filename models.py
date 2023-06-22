from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, DECIMAL, Boolean
from loader import engine, Base
from sqlalchemy.orm import relationship
from datetime import datetime


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True)
    user_name = Column(String)
    full_name = Column(String)
    registration_date = Column(DateTime, default=datetime.utcnow)
    balance = Column(DECIMAL)
    actyvity = Column(Boolean)  # Оплачен/активирован ли аккаунт. По умолчания False
    messages = relationship("Messages",  back_populates="user")
    orders = relationship("Order", back_populates="user")

class Messages(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, ForeignKey('users.telegram_id'))
    date_message = Column(DateTime, default=datetime.utcnow)
    text_message = Column(String)
    user = relationship("User", back_populates="messages")

class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    category_name = Column(String, unique=True)
    products = relationship("Product", back_populates="category")

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey('category.id'))
    product_name = Column(String)
    product = Column(String) # Продуктом является цифровой ключ
    price = Column(DECIMAL)
    amount = Column(Integer)
    order_items = relationship("Order_items", back_populates="product")
    category = relationship("Category", back_populates="products")

class Order(Base):  # Корзина
    __tablename__ = 'orders'
    order_id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, ForeignKey('users.telegram_id'))
    user = relationship("User", back_populates="orders")
    date_order = Column(DateTime, default=datetime.utcnow)
    status_order = Column(Boolean)
    order_items = relationship("Order_items", back_populates="order")
    payments = relationship("Payment", back_populates="order")

class Order_items(Base):  # Элементы корзины
    __tablename__ = 'order_items'
    order_item_id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.order_id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    product = relationship("Product", back_populates="order_items")
    order = relationship("Order", back_populates="order_items")
    amount = Column(Integer)

class Payment(Base):
    __tablename__ = 'payments'
    payment_id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.order_id"))
    order = relationship("Order", back_populates="payments")
    amount_to_pay = Column(DECIMAL)
    payment_method = Column(String)
    status_payment = Column(Boolean)


Base.metadata.create_all(engine)