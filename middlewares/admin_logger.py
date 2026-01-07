from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message
from database.crud.admins import get_is_admin, add_admin_log



class AdminLoggerMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        result = await handler(event, data)

        # логируем только callback / message
        if not isinstance(event, (CallbackQuery, Message)):
            return result

        user = event.from_user
        if not user:
            return result

        admin = await get_is_admin(user.id)
        if not admin:
            return result  # не админ — не логируем

        # формируем действие
        if isinstance(event, CallbackQuery):
            action = f"callback:{event.data}"
        else:
            action = f"message:{event.text}"

        await add_admin_log(
            admin_id=admin.id,
            action=action
        )

        return result