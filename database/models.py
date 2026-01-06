from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from sqlalchemy.types import BIGINT, String, DateTime, Text, Numeric, Boolean, Integer
from database.session import engine
from datetime import datetime
from typing import Optional
from decimal import Decimal


class Base(DeclarativeBase):
    pass


#Таблица Users
class Users(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    username: Mapped[Optional[str]] = mapped_column(String(40))
    first_name: Mapped[str] = mapped_column(String)
    last_name: Mapped[Optional[str]] = mapped_column(String)
    created_ad: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())

    cart = relationship("Cart", back_populates="user")
    order = relationship("Orders", back_populates="user")
    admin = relationship("Admins", back_populates="user")


#Таблица админов
class Admins(Base):
    __tablename__ = "admins"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    role: Mapped[str] = mapped_column(String(30))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())

    user = relationship("Users", back_populates="admin")
    log = relationship("LogAdmins", back_populates="admin")


#Таблиц действий админов
class LogAdmins(Base):
    __tablename__ = "log_admins"

    id: Mapped[int] = mapped_column(primary_key=True)
    admin_id: Mapped[int] = mapped_column(ForeignKey("admins.id"))
    action: Mapped[str] = mapped_column(String)

    admin = relationship("Admins", back_populates="log")


#Таблица Categories
class Categories(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)
    # Связь: в категории много товаров
    product = relationship("Products", back_populates="category")


#Таблица Products
class Products(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(Text)
    price: Mapped[Decimal] = mapped_column(Numeric(10,2))
    image_url: Mapped[str] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())

    category = relationship("Categories", back_populates="product")
    cart = relationship("Cart", back_populates="product")


#Таблица Cart
class Cart(Base):
    __tablename__ = 'cart'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'))
    quantity: Mapped[int] = mapped_column(Integer)

    user = relationship("Users", back_populates="cart")
    product = relationship("Products", back_populates="cart")


#Таблица Orders
class Orders(Base):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    total_price: Mapped[float] = mapped_column(Numeric(10, 2))
    status: Mapped[str] = mapped_column(String(30))
    payment_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())

    user = relationship("Users", back_populates="order")
    order_item = relationship("Order_items", back_populates="order")


#Таблица Order_items
class Order_items(Base):
    __tablename__ = 'order_items'

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey('orders.id'))
    product_name: Mapped[str] = mapped_column()
    price: Mapped[float] = mapped_column(Numeric(10,2))
    quantity: Mapped[int] = mapped_column(Integer)

    order = relationship("Orders", back_populates="order_item")


async def create_table():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)