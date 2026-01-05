from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder



#Подтверждение товаров в корзине
kb_orders_confirmation = InlineKeyboardMarkup(inline_keyboard=[    
    [InlineKeyboardButton(text="✅ Далее", callback_data="order_next"),
    InlineKeyboardButton(text="❌ Отмена", callback_data="cart")]
])


#Кнопки отмены или продолжения оплаты заказа
async def kb_payment(order_id: int):
    builder = InlineKeyboardBuilder()

    builder.button(text="💳Оплата", callback_data=f"payment:{order_id}")
    builder.button(text="❌Отменить", callback_data=f"cancel:{order_id}")
    builder.as_markup()

    return builder.as_markup()