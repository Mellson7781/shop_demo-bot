from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command
from database.crud.admins import get_is_admin
from services.status import AdminsRole
from keyboards.inline.admins import menu_manager, menu_senior, menu_super


cmd_admin_rt = Router()


#Менеджер меню
@cmd_admin_rt.message(Command("managers"))
async def is_manager(message: Message):
    user_id = message.from_user.id
    admin = await get_is_admin(user_id)

    if admin is None:
        await message.answer("🚫Отказано в доступе!")
        return
    
    await message.answer("🗃Выберете категорию заказа",
                         reply_markup=menu_manager)
   

#Меню старшего менеджера
@cmd_admin_rt.message(Command("senior"))
async def is_senior(message: Message):
    user_id = message.from_user.id
    admin = await get_is_admin(user_id)

    if admin.role not in [AdminsRole.SENIOR.value, AdminsRole.SUPER.value]:
        await message.answer("🚫Отказано в доступе!")
        return
    
    await message.answer("🗃Выберете список действий",
                         reply_markup=menu_senior)
    

#Меню супер админа
@cmd_admin_rt.message(Command("super"))
async def is_super(message: Message):
    user_id = message.from_user.id
    admin = await get_is_admin(user_id)

    if admin.role != AdminsRole.SUPER.value:
        await message.answer("🚫Отказано в доступе!")
        return
    
    await message.answer("🗃Выберете список действий",
                         reply_markup=menu_super)