from sqlalchemy import select, update, delete
from database.session import AsyncSessionLocal
from database.models import Admins, Orders, Order_items, Users, Products, LogAdmins
from services.status import AdminsRole


#Проверка на админа
async def get_is_admin(user_id: int) -> Admins | None:
    async with AsyncSessionLocal() as session:
        async with session.begin():
            admin = await session.scalars(
                select(Admins)
                .where(Admins.user_id == user_id)
            )
            return admin.first()


#Получение всех админов
async def get_all_admins() -> list[Admins]:
    async with AsyncSessionLocal() as session:
        async with session.begin():
            admins = await session.scalars(
                select(Admins)
            )
            return admins.all()


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


#Получение пользователя по username
async def get_user_by_usename(username: str) -> Users | None:
    async with AsyncSessionLocal() as session:
        result = await session.scalar(select(Users)
                                      .where(Users.username == username))
        return result


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


#Добавить нового админа
async def add_new_admin(
        user_id: int,
        username: str,
):
    async with AsyncSessionLocal() as session:
        async with session.begin():
            admin = Admins(
                user_id = user_id,
                username = username,
                role = AdminsRole.MANAGER.value
            )
            session.add(admin)


#Проверка на админа по id
async def get_is_admin_by_id(admin_id: int) -> Admins | None:
    async with AsyncSessionLocal() as session:
        async with session.begin():
            admin = await session.scalars(
                select(Admins)
                .where(Admins.id == admin_id)
            )
            return admin.first()


#Удаление админа из бд
async def del_admin_by_id(admin_id: int) -> bool:
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            delete(Admins)
            .where(Admins.id == admin_id)
        )

        await session.commit()
        return result.rowcount > 0


#Получение всех админов
async def all_admins_active() -> list[LogAdmins]:
    async with AsyncSessionLocal() as session:
        async with session.begin():
            result = await session.scalars(
                select(LogAdmins)
            )
            return result.all()


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


async def all_admins_active():
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(
                LogAdmins.id,
                LogAdmins.action,
                LogAdmins.created_at,
                Admins.username,
                Admins.role
            )
            .join(Admins, Admins.id == LogAdmins.admin_id)
            .order_by(LogAdmins.created_at.desc())
        )
        return result.all()


#Логи
async def add_admin_log(admin_id: int, action: str):
    async with AsyncSessionLocal() as session:
        async with session.begin():
            session.add(
                LogAdmins(
                    admin_id=admin_id,
                    action=action
                )
            )