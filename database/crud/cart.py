from sqlalchemy import select, update, delete, and_
from database.session import AsyncSessionLocal
from database.models import Products, Cart


#Добавление товара в корзину
async def add_in_cart(
        user_id: int, product_id: int        
):
    async with AsyncSessionLocal() as session:
        async with AsyncSessionLocal() as session:
            async with session.begin():
                in_cart = await session.scalars(
                    select(Cart).where(
                        and_(Cart.user_id == user_id, Cart.product_id == product_id)
                    )
                )
                cart_item = in_cart.first()

                if cart_item is None:
                    session.add(Cart(user_id=user_id, product_id=product_id, quantity=1))
                else:
                    await session.execute(
                        update(Cart)
                        .where(and_(Cart.user_id == user_id, Cart.product_id == product_id))
                        .values(quantity=cart_item.quantity + 1)
                    )
                    

#Показать корзину конкретного пользователя
async def user_cart(id: int) -> list[Cart]:
    async with AsyncSessionLocal() as session:
        async with session.begin():
            cart = await session.scalars(select(Cart)
                                .where(
                                Cart.user_id == id
                                ))
            
            return cart.all()
        
    
#Получение всех товаров из корзины пользователя
async def get_products_in_cart(user_id: int) -> list[Products]:
    async with AsyncSessionLocal() as session:
        async with session.begin():
            products = await session.scalars(
                select(Products)
                .join(Cart)
                .where(Cart.user_id == user_id)
                )
            return products.all()


#Показать элемент из корзины по id
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
            
            cart_item = await get_cart(id)

            if cart_item.quantity < 1:
                await cart_product_del(id)


#Удаление товара из корзины
async def cart_product_del(id: int):
    async with AsyncSessionLocal() as session:
        async with session.begin():
            await session.execute(
                    delete(Cart)
                    .where(Cart.id == id))