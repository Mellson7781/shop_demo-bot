from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database.crud import (get_categories, get_products_in_cat,
                           user_cart, get_product)


#Меню товаров в корзине
async def kb_cart_menu(id: int):
    builder = InlineKeyboardBuilder()
    cart = await user_cart(id)

    for item in cart:
        product = await get_product(id = item.product_id)

        if product.is_active:
            builder.button(text=f"{product.name} || {item.quantity}шт",
                           callback_data=f"cart_pr:{item.id}")
    if not cart:
        builder.button(text="🏷Перейти в каталог",
                       callback_data="catalog")
    else:
        builder.button(text="Оформить заказ 📄",
                       callback_data="order_start")
        
    builder.adjust(1)
    return builder.as_markup()


#Управление товаром в корзине
async def kb_in_cart_prod(id: int):
    builder = InlineKeyboardBuilder()

    builder.button(text='➕', 
                          callback_data=f'+:{id}')
    builder.button(text='❌',
                   callback_data=f'delete_pr:{id}')
    builder.button(text='➖', 
                          callback_data=f'-:{id}')
    builder.button(text=f"🔙 Назад к корзине",
                   callback_data="cart")
    
    builder.adjust(3,1)
    
    return builder.as_markup()


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