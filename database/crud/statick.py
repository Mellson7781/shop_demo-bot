from sqlalchemy import select, update, delete
from database.session import AsyncSessionLocal
from database.models import (Users, Categories, 
                             Products, Cart, 
                             Orders, Order_items)


#Получение всех заказов пользователя
async def get_orders(id: int) -> list[Orders]:
    async with AsyncSessionLocal() as session:
        async with session.begin():
            order = await session.scalars(select(Orders)
                                          .where(Orders.user_id == id))
            return order.all()
