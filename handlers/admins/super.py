from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from services.status import AdminsRole
from database.crud.admins import (
    get_is_admin,
    get_all_admins,
    get_user_by_usename,
    add_new_admin,
    get_is_admin_by_id,
    del_admin_by_id, 
    all_admins_active
)
from keyboards.inline.admins import menu_super, delete_or_create_admin, back_super
from states.admin import AddAdmin, DelAdmin
from middlewares.admin_check import SuperMiddleware
from middlewares.admin_logger import AdminLoggerMiddleware

super_rt = Router()


super_rt.callback_query.middleware(SuperMiddleware())
super_rt.callback_query.middleware(AdminLoggerMiddleware())
super_rt.message.middleware(AdminLoggerMiddleware())


# =======================
# Обработка кнопки "Назад"
# =======================
@super_rt.callback_query(F.data == "super")
async def back(query: CallbackQuery):
    await query.message.delete()
    await query.message.answer("🗃Выберете пункт меню:",
                         reply_markup=menu_super)
    

# =======================
# Обработка кнопки "Админы"
# =======================
@super_rt.callback_query(F.data == "list_admins")
async def edit_admin(query: CallbackQuery):
    admins = await get_all_admins()

    if not admins:
        await query.answer(
            "Админы не найдены!",
            show_alert=True
        )

    await query.message.delete()

    text = "💻Список админов:\n\n"
    for admin in admins:
        text += (f"🫆Админ №{admin.id} - Роль: {admin.role}\n"
        f"🛃Username: @{admin.username}\n"
        f"⚠️Id: {admin.user_id}\n\n")

    await query.message.answer(
        text,
        reply_markup=delete_or_create_admin)
    

# =======================
# Обработка кнопки "Добавить"
# =======================
@super_rt.callback_query(F.data == "add_admin")
async def add_admin(query: CallbackQuery, state: FSMContext):
    await query.message.delete()
    await query.message.answer("✅Напишите username пользователя которого хотите назначить:")
    await state.set_state(AddAdmin.username)


# =======================
# Обработка AddAdmin.username 
# =======================
@super_rt.message(AddAdmin.username)
async def add_admin_states(message: Message, state: FSMContext):
    username = message.text
    username = username[1:]

    user = await get_user_by_usename(username)

    if not user:
        await message.answer(
            "⚠️Мы не нашли такого пользователя!",
            reply_markup = back_super
        )
        return
    
    admin = await get_is_admin(user.id)

    if admin:
        await message.answer(
            "⚠️Этот пользователь уже админ!",
            reply_markup = back_super
        )
        return
    
    await add_new_admin(user.id, user.username)

    await message.answer("✅Новый админ добавлен!")
    await state.clear()

# =======================
# Обработка кнопки "Удалить"
# =======================
@super_rt.callback_query(F.data == "del_admin")
async def del_admin(query: CallbackQuery, state: FSMContext):
    await query.message.delete()
    await query.message.answer("❌Напишите №id админа которого хотите снять:")
    await state.set_state(DelAdmin.username)


# =======================
# Обработка DelAdmin.username 
# =======================
@super_rt.message(DelAdmin.username)
async def del_admin_states(message: Message, state: FSMContext):
    try:
        admin_id = int(message.text)
    except ValueError:
        await message.answer("⚠️Вы написали не id этого админа!", reply_markup=back_super)
        return

    admin = await get_is_admin_by_id(admin_id)

    if not admin:
        await message.answer(
            "⚠️Мы не нашли такого администратора!",
            reply_markup = back_super
        )
        return
    
    if admin.role == AdminsRole.SUPER.value:
        await message.answer(
            "⚠️Этого администратора нельзя снять!",
            reply_markup = back_super
        )
        return
    
    res = await del_admin_by_id(admin_id)

    if not res:
        await message.answer(
            "⚠️Не удалось снять администратора!",
            reply_markup = back_super
        )
        return

    await message.answer("❌Админ снят с должности!")
    await state.clear()


# =======================
# Список действий админов
# =======================
@super_rt.callback_query(F.data == "admins_active")
async def list_admins_active(query: CallbackQuery):
    rows = await all_admins_active()
    await query.message.delete()
    await query.answer("")

    if not rows:
        await query.message.answer(
            "⚠️ Пока нет никаких действий!",
            reply_markup=back_super
        )
        return

    text = "🗒 Список действий:\n\n"
    for i, row in enumerate(rows, start=1):
        text += (
            f"#{i}\n"
            f"👤 @{row.username} ({row.role})\n"
            f"📝 {row.action}\n"
            f"📆 {row.created_at}\n\n"
        )

    await query.message.answer(text, reply_markup=back_super)