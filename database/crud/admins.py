from sqlalchemy import select, update
from database.session import AsyncSessionLocal
from database.models import Admins


#Проверка на админа
async def get_is_admin(user_id: int) -> Admins | None:
    async with AsyncSessionLocal() as session:
        async with session.begin():
            admin = await session.scalars(
                select(Admins)
                .where(Admins.user_id == user_id)
            )
            return admin.first()