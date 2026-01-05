from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder



#Подтверждение товаров в корзине
kb_orders_confirmation = InlineKeyboardMarkup(inline_keyboard=[    
    [InlineKeyboardButton(text="✅ Далее", callback_data="order_next"),
    InlineKeyboardButton(text="❌ Отмена", callback_data="cart")]
])


#Кнопка перевода к оплате
async def kb_payment(order_id: int):
    builder = InlineKeyboardBuilder()

    builder.button(text="💳Оплата", callback_data=f"payment:{order_id}")
    return builder.as_markup()