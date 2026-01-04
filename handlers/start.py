from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from database.crud.users import get_user_by_id, new_user_add
from keyboards.reply import main_menu_kb


#Роутер start
start_rt = Router()


#Обработка команды старт
@start_rt.message(CommandStart())
async def start(message: Message):
    user_id = message.from_user.id

    if await get_user_by_id(user_id) is None:
        await new_user_add(
            id=user_id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name
            )
        
    await message.answer("👋 Добро пожаловать в магазин!"
                         "\nВыберите действие:",
                         reply_markup=main_menu_kb())