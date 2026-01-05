from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


#Кнопка статусов заказа
kb_filter_my_order = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="💰На оплату", 
                          callback_data="for_payment")],
    [InlineKeyboardButton(text="❌Не завершенные", 
                          callback_data="not_completed")],
    [InlineKeyboardButton(text="✅Завершенные", 
                          callback_data="completed")]
])


#Кнопка назад
back_menu_my_orders = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Назад 🔙', 
                              callback_data="my_orders")]
])


#Список заказов
async def kb_list_of_orders(orders_id: list):
    builder = InlineKeyboardBuilder()
    orders = orders_id

    for i in orders:
        builder.button(text=f"Заказ №{i}",
                       callback_data=f"order:{i}")
        
    builder.button(text='Назад 🔙', callback_data="my_orders")
    builder.adjust(1)

    return builder.as_markup()