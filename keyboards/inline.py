from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database.crud import (get_categories, get_products_in_cat,
                           user_cart, get_product)


#Меню категорий
async def kb_menu_categories():
    builder = InlineKeyboardBuilder()
    list_ct = await get_categories()

    #Создание кнопок категории из списка
    for but in list_ct:
        builder.button(text=but.name, 
                       callback_data=f'cat_{but.id}')
    
    builder.adjust(2)
    return builder.as_markup()


#Меню товаров в категории
async def kb_product_in_cat(id: int):
    builder = InlineKeyboardBuilder()
    products = await get_products_in_cat(id)

    for item in products:
        if item.is_active:
            builder.button(text=item.name, 
                       callback_data=f"product_{item.id}")
    
    builder.button(text="🔙 Назад к категориям",
                   callback_data="back_cat")
    builder.adjust(1)
    return builder.as_markup()


#Меню действий с карточкой товара
async def kb_in_product(id: int):
    builder = InlineKeyboardBuilder()

    builder.button(text='➕ Добавить в корзину', 
                          callback_data=f'add_basket:{id}')
    builder.button(text='🔙 Назад к категориям',
                   callback_data=f'back_cat')
    
    builder.adjust(1)
    
    return builder.as_markup()


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