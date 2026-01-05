from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


#Подтверждение товаров в корзине
kb_orders_confirmation = InlineKeyboardMarkup(inline_keyboard=[    
    [InlineKeyboardButton(text="✅ Далее", callback_data="order_next"),
    InlineKeyboardButton(text="❌ Отмена", callback_data="cart")]
])


#Подтверждение заказа
kb_orders_payment_conf = InlineKeyboardMarkup(inline_keyboard=[    
    [InlineKeyboardButton(text="✅ Да", callback_data="order_payment"),
    InlineKeyboardButton(text="❌ Нет", callback_data="cart")]
])


#Подтверждение заказа
kb_orders_payment_conf = InlineKeyboardMarkup(inline_keyboard=[    
    [InlineKeyboardButton(text="✅ Да", callback_data="order_payment"),
    InlineKeyboardButton(text="❌ Нет", callback_data="cart")]
])


#Способы оплаты
async def kb_payment(order_id: int):
    builder = InlineKeyboardBuilder()

    builder.button(text="💳Оплата", callback_data=f"payment:{order_id}")
    return builder.as_markup()


#Кнопка статусов заказа
kb_filter_my_order = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="✅Завершенные", callback_data="completed"),
     InlineKeyboardButton(text="❌Не завершенные", callback_data="not_completed")]
])