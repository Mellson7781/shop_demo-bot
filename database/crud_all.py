from sqlalchemy import select, update, delete
from database.session import AsyncSessionLocal
from database.models import (Users, Categories, 
                             Products, Cart, 
                             Orders, Order_items)

#Добавление товара в корзину
async def add_in_cart(
        user_id: int, product_id: int        
):
    async with AsyncSessionLocal() as session:
        async with session.begin():
            in_cart = await session.scalars(select(Cart)
                                .where(
                                    Cart.user_id == user_id,
                                    Cart.product_id == product_id))
            cart_item = in_cart.first() 
            if cart_item is None:
                product = Cart(user_id = user_id,
                              product_id = product_id,
                              quantity = 1)
                session.add(product)
            else:
                await session.execute(
                    update(Cart)
                    .where(Cart.user_id == user_id, 
                          Cart.product_id == product_id)
                    .values(quantity = cart_item.quantity + 1))


#Показать корзину конкретного пользователя
async def user_cart(id: int) -> list[Cart]:
    async with AsyncSessionLocal() as session:
        async with session.begin():
            cart = await session.scalars(select(Cart)
                                .where(
                                Cart.user_id == id
                                ))
            
            return cart.all()


#Покказать элемент из корзины по id
async def get_cart(id: int) -> Cart | None:
    async with AsyncSessionLocal() as session:
        async with session.begin():
            result = await session.scalars(select(Cart)
                                            .where(
                                                Cart.id == id
                                            ))
            return result.first()

#Добавление товара в корзине по id
async def cart_plus(id: int):
    async with AsyncSessionLocal() as session:
        async with session.begin():
            await session.execute(
                    update(Cart)
                    .where(Cart.id == id)
                    .values(quantity = Cart.quantity + 1))


#Убавление товара в корзине по id
async def cart_minus(id: int):
    async with AsyncSessionLocal() as session:
        async with session.begin():
            await session.execute(
                    update(Cart)
                    .where(Cart.id == id)
                    .values(quantity = Cart.quantity - 1))


#Удаление товара из корзины
async def cart_product_del(id: int):
    async with AsyncSessionLocal() as session:
        async with session.begin():
            await session.execute(
                    delete(Cart)
                    .where(Cart.id == id))


#Добавление заказа в бд
async def create_order(user_id: int, 
                       name: str, contact: str,
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
                name = name,
                contact = contact,
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
            
        return order.id


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
            

#Получение всех заказов пользователя
async def get_orders(id: int) -> list[Orders]:
    async with AsyncSessionLocal() as session:
        async with session.begin():
            order = await session.scalars(select(Orders)
                                          .where(Orders.user_id == id))
            return order.all()
