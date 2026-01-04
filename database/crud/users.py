from sqlalchemy import select
from database.session import AsyncSessionLocal
from database.models import Users


#Получение пользователя по tg id
async def get_user_by_id(tg_id: int) -> Users | None:
    async with AsyncSessionLocal() as session:
        result = await session.scalar(select(Users)
                                      .where(Users.id == tg_id))
        return result


#Добавление пользователя в бд
async def new_user_add(
    id: int,
    username: str,
    first_name: str,
    last_name: str
):
    async with AsyncSessionLocal() as session:
        async with session.begin():
            user = Users(
                id=id,
                username=username,
                first_name=first_name,
                last_name=last_name
            )
            session.add(user)
