from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command
from database.crud.users import get_user_by_id
from database.crud.admins import get_is_admin
from services.status import AdminsRole
from keyboards.inline.admins import menu_manager, menu_super


cmd_admin_rt = Router()


#Менеджер меню
@cmd_admin_rt.message(Command("managers"))
async def is_manager(message: Message):
    user_id = message.from_user.id

    if not await get_user_by_id(user_id):
        await message.answer("Сначала напишите команду /start!")
        return
    
    admin = await get_is_admin(user_id)

    if admin is None:
        await message.answer("🚫Отказано в доступе!")
        return
    
    await message.answer("🗃Выберете категорию заказа",
                         reply_markup=menu_manager)
   
    
#Меню супер админа
@cmd_admin_rt.message(Command("super"))
async def is_super(message: Message):
    user_id = message.from_user.id

    if not await get_user_by_id(user_id):
        await message.answer("Сначала напишите команду /start!")
        return
    
    admin = await get_is_admin(user_id)

    if not admin:
        await message.answer("🚫Отказано в доступе!")
        return

    if admin.role != AdminsRole.SUPER.value:
        await message.answer("🚫Отказано в доступе!")
        return
    
    await message.answer("🗃Выберете пункт меню:",
                         reply_markup=menu_super)