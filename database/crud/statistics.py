from sqlalchemy import select, and_
from database.session import AsyncSessionLocal
from database.models import Orders, Order_items


#Получение всех заказов пользователя
async def get_orders(id: int) -> list[Orders]:
    async with AsyncSessionLocal() as session:
        async with session.begin():
            order = await session.scalars(select(Orders)
                                          .where(Orders.user_id == id))
            return order.all()


#Получение заказов по user_id и статусу
async def status_get_order(user_id: int, status: str) -> list[Orders]:
    async with AsyncSessionLocal() as session:
        async with session.begin():
            orders = await session.scalars(select(Orders)
                        .where(and_(Orders.user_id == user_id, 
                             Orders.status == status))
            )
            return orders.all()


#Получение всех элементов заказа
async def get_order_items(order_id: int) -> list[Order_items]:
       async with AsyncSessionLocal() as session:
        async with session.begin():
            order_items = await session.scalars(select(Order_items)
                        .where(Order_items.order_id == order_id)
            )
            return order_items.all()