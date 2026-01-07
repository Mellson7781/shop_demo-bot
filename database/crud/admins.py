from sqlalchemy import select, update
from database.session import AsyncSessionLocal
from database.models import Admins, Orders, Order_items, Users, Products
from services.status import OrderStatus


#Проверка на админа
async def get_is_admin(user_id: int) -> Admins | None:
    async with AsyncSessionLocal() as session:
        async with session.begin():
            admin = await session.scalars(
                select(Admins)
                .where(Admins.user_id == user_id)
            )
            return admin.first()


#Получение заказов по статусу
async def status_get_order(status: str) -> list[Orders]:
    async with AsyncSessionLocal() as session:
        async with session.begin():
            orders = await session.scalars(select(Orders)
                        .where(Orders.status == status))
            return orders.all()
        

#Получение заказа по id
async def get_order(id: int) -> Orders | None:
    async with AsyncSessionLocal() as session:
        async with session.begin():
            order = await session.scalars(select(Orders)
                                          .where(Orders.id == id))
            return order.first()


#Получение всех элементов заказа
async def get_order_items(order_id: int) -> list[Order_items]:
       async with AsyncSessionLocal() as session:
        async with session.begin():
            order_items = await session.scalars(select(Order_items)
                        .where(Order_items.order_id == order_id)
            )
            return order_items.all()


#Получение пользователя по id заказа
async def get_user_by_order_id(order_id: int) -> Users:
    async with AsyncSessionLocal() as session:
        async with session.begin():
            user = await session.scalars(
                select(Users)
                .join(Users.order)
                .where(Orders.id == order_id)
                )
            return user.first()


#Изменение статуса пользователя
async def update_order_status(order_id: int, next_status: str) -> bool:
    async with AsyncSessionLocal() as session:
            result = await session.execute(
                update(Orders)
                .where(Orders.id == order_id)
                .values(status = next_status)
            )
            await session.commit()

            return result.rowcount > 0


#Получение конкретного товара по id
async def get_product(id: int) -> Products:
    async with AsyncSessionLocal() as session:
        result =  await session.scalars(select(Products)
                                     .where(Products.id == id))
        return result.first()


#Скрыть\показать товар
async def update_product_status(product_id: int, res: bool) -> bool:
    async with AsyncSessionLocal() as session:
            result = await session.execute(
                update(Products)
                .where(Products.id == product_id)
                .values(is_active = res)
            )
            await session.commit()

            return result.rowcount > 0