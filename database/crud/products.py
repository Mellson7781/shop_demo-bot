from sqlalchemy import select
from database.session import AsyncSessionLocal
from database.models import Products

#Получение конкретного товара по id
async def get_product(id: int) -> Products:
    async with AsyncSessionLocal() as session:
        result =  await session.scalars(select(Products)
                                     .where(Products.id == id))
        return result.first()