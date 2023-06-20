from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, DECIMAL, Boolean
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

engine = create_engine('sqlite:///DataBase.db')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True)
    user_name = Column(String)
    full_name = Column(String)
    registration_date = Column(DateTime, default=datetime.utcnow)
    balance = Column(DECIMAL)
    actyvity = Column(Boolean)  # Оплачен/активирован ли аккаунт. По умолчания False
    messages = relationship("Message",  back_populates="user", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="user", cascade="all, delete-orphan")


class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.telegram_id'))
    date_message = Column(DateTime, default=datetime.utcnow)
    text_message = Column(String)
    user = relationship("User", back_populates="messages")


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    product_name = Column(String)
    product = Column(String) # Продуктом является цифровой ключ
    price = Column(DECIMAL)
    order_items = relationship("Order_items", back_populates="product", cascade="all, delete-orphan")  # Changed 'products' to 'product'


class Order(Base):  # Корзина
    __tablename__ = 'orders'
    order_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.telegram_id'))
    user = relationship("User", back_populates="orders")
    date_order = Column(DateTime, default=datetime.utcnow)
    status_order = Column(Boolean)
    order_items = relationship("Order_items", back_populates="order", cascade="all, delete-orphan")
    payments = relationship("Payment", back_populates="order", cascade="all, delete-orphan")

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