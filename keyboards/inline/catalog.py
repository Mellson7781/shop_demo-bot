from aiogram.utils.keyboard import InlineKeyboardBuilder
from database.crud.catalog import get_categories, get_products_in_cat


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