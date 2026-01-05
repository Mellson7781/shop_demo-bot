from sqlalchemy import select, update, and_
from database.session import AsyncSessionLocal
from database.models import Products, Orders, Order_items
from database.crud.cart import user_cart


#Добавление заказа в бд
async def create_order(user_id: int, 
                       total_price: float):
    async with AsyncSessionLocal() as session:
        async with session.begin():
            #Получение корзины пользователя
            cart_items = await user_cart(user_id)

            #Проверка корзины
            if not cart_items:
                raise ValueError("Корзина пуста")
            
            #Создание заказа
            order = Orders(
                user_id=user_id,
                total_price = total_price,
                status = "created",
                payment_id = ""
            )
            session.add(order)
            await session.flush()

            # 3. Создаём order_items
            for item in cart_items:
                price = await session.scalar(
                select(Products.price)
                .where(Products.id == item.product_id))

                order_item = Order_items(
                    order_id=order.id,
                    product_id=item.product_id,
                    price=price,
                    quantity=item.quantity
                )
                session.add(order_item)

            # 4 Очистка корзины
            for item in cart_items:
                await session.delete(item)

            
            # 5 Возврат созданного заказа
            return order


#Получение заказа по id
async def get_order(id: int) -> Orders | None:
    async with AsyncSessionLocal() as session:
        async with session.begin():
            order = await session.scalars(select(Orders)
                                          .where(Orders.id == id))
            return order.first()


#Изменение статуса у заказа на оплачено по id
async def order_status_paid(id: int, pay_id: str):
    async with AsyncSessionLocal() as session:
        async with session.begin():
            order = await get_order(id)

            if order.status != "created":
                raise ValueError("status not created!")
            
            await session.execute(
                    update(Orders)
                    .where(Orders.id == id)
                    .values(status = "paid", payment_id = pay_id))


#Изменение статуса у заказов на отмененый
async def order_status_canel(user_id: int):
    async with AsyncSessionLocal() as session:
        async with session.begin():
            await session.execute(
                    update(Orders)
                    .where(Orders.user_id == user_id,
                           Orders.status == "created")
                    .values(status = "canel"))


#Получение заказа по user_id
async def get_order_user(user_id: int) -> Orders | None:
    async with AsyncSessionLocal() as session:
        async with session.begin():
            order = await session.scalars(select(Orders)
                        .where(and_(Orders.user_id == user_id, 
                             Orders.status == "created"))
            )
            return order.first()