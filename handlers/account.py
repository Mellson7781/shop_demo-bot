from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from database.crud.users import get_user_by_id, update_info_user
from keyboards.inline.account import button_update


account_rt = Router()


#Кнопка аккаунт
@account_rt.message(F.text == "🃏 Аккаунт")
async def account_info(message: Message):
    user_id = message.from_user.id
    user = await get_user_by_id(user_id)

    if user is None:
        await message.answer("Упс, не можем найти ваш аккаунт🤖!")
        return

    def is_none(text: str | None) -> str:
        if text is None:
            return "Нет"
        return text
    
    await message.answer(
            "⚠️Аккаунт:\n"
            f"💻Username: @{is_none(user.username)}\n"
            f"1️⃣Первое имя: {user.first_name}\n"
            f"🔟Последние имя: {is_none(user.last_name)}\n"
            f"📆Создан: {user.created_ad}",
            reply_markup = button_update
            )


#Обновление данных
@account_rt.callback_query(F.data.startswith("update_info"))
async def update_info(query: CallbackQuery):
    user_id = query.from_user.id
    username = query.from_user.username
    last_name = query.from_user.last_name
    print(query.from_user.last_name)
    await update_info_user(
        user_id, username, last_name
        )

    await query.answer("Данные обновлены",
                       show_alert=True)

    user = await get_user_by_id(user_id)

    def is_none(text: str | None) -> str:
        if text is None:
            return "Нет"
        return text
    
    await query.message.delete()
    await query.message.answer(
            "⚠️Аккаунт:\n"
            f"💻Username: @{is_none(user.username)}\n"
            f"1️⃣Первое имя: {user.first_name}\n"
            f"🔟Последние имя: {is_none(user.last_name)}\n"
            f"📆Создан: {user.created_ad}",
            reply_markup = button_update
            )