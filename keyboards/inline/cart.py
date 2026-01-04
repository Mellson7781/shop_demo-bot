from aiogram.utils.keyboard import InlineKeyboardBuilder
from database.crud.cart import user_cart, get_products_in_cart


#Меню товаров в корзине
async def kb_cart_menu(id: int):
    builder = InlineKeyboardBuilder()
    cart = await user_cart(id)
    products = await get_products_in_cart(id)

    if not cart:
        builder.button(text="🏷Перейти в каталог",
                       callback_data="catalog")
        
    product_map = {p.id: p for p in products}

    for item in cart:
        product = product_map.get(item.product_id)

        if product.is_active:
            builder.button(text=f"{product.name} || {item.quantity}шт",
                           callback_data=f"cart_pr:{item.id}")
            
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