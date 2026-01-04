from sqlalchemy import select
from database.session import AsyncSessionLocal
from database.models import Categories, Products


#Получение всех категорий
async def get_categories() -> list[Categories]:
    async with AsyncSessionLocal() as session:
        result = await session.scalars(select(Categories))
        return result.all()


#Получение всех товаров из категории
async def get_products_in_cat(id: int) -> list[Products]:
    async with AsyncSessionLocal() as session:
        result = await session.scalars(select(Products)
                                     .where(Products.category_id == id))
        return result.all()
    

#Получение конкретного товара по id
async def get_product(id: int) -> Products:
    async with AsyncSessionLocal() as session:
        result =  await session.scalars(select(Products)
                                     .where(Products.id == id))
        return result.first()