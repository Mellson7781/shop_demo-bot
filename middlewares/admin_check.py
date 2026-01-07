from aiogram import BaseMiddleware
from database.crud.admins import get_is_admin
from services.status import AdminsRole


# =======================
# Middleware администратора роли: SUPER
# =======================
class SuperMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        user_id = event.from_user.id
        admin = await get_is_admin(user_id)
        if not admin:
            if hasattr(event, "answer"):
                await event.answer("🚫 Отказано в доступе!", show_alert=True)
            return
        if admin.role != AdminsRole.SUPER.value:
            if hasattr(event, "answer"):
                await event.answer("🚫 Отказано в доступе!", show_alert=True)
            return
        return await handler(event, data)


# =======================
# Middleware администратора
# =======================
class AdminMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        user_id = event.from_user.id
        if not await get_is_admin(user_id):
            if hasattr(event, "answer"):
                await event.answer("🚫 Отказано в доступе!", show_alert=True)
            return
        return await handler(event, data)