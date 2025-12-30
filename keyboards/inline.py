from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database.crud import get_categories


#Меню категорий
async def kb_menu_categories():
    builder = InlineKeyboardBuilder()
    list_ct = await get_categories()

    #Создание кнопок категории из списка
    for but in list_ct:
        builder.button(text=but.name, callback_data=f'cat_{but.id}')
    
    builder.adjust(2)
    return builder.as_markup()


#Кнопка назад  
async def menu_back(data:str):
    builder = InlineKeyboardBuilder()

    builder.button(text='Назад🔙', callback_data=f'back_{data}')
    return builder.as_markup()


#Кнопка Добавить в корзину
menu_add_basket = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='➕ Добавить в корзину', 
                          callback_data='add_basket')]
])