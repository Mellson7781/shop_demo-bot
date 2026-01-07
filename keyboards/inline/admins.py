from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from services.status import OrderStatus
from database.crud.catalog import get_categories, get_products_in_cat


#Админ меню для менеджера
menu_manager = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🛒Новые",
                callback_data="created")],
        [InlineKeyboardButton(text="💰Оплаченные",
                callback_data="paid")],
        [InlineKeyboardButton(text="✅Активные",
                callback_data="assembled")],
        [InlineKeyboardButton(text="🗂Завершённые",
                callback_data="adm_completed")],
        [InlineKeyboardButton(text="🛒Товары",
                callback_data="admins_products")]
    ]
)


#Кнопка назад для менеджеров
button_back = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Назад🔙",
                              callback_data="manager")]
    ]
)


#Список заказов
async def kb_list_of_orders(orders_id: list, data: str):
    builder = InlineKeyboardBuilder()
    orders = orders_id

    for i in orders:
        builder.button(text=f"Заказ №{i}",
                       callback_data=f"order_adm:{data}:{i}")
        
    builder.button(text='Назад🔙', callback_data="manager")
    builder.adjust(1)

    return builder.as_markup()


#Меню заказа
async def kb_status(order_id: int, status: str):
    builder = InlineKeyboardBuilder()

    if status not in [OrderStatus.COMPLEDET.value, OrderStatus.CREATED.value]:
        builder.button(text=f"🔜Перевсти в следующий статус",
                       callback_data=f"next:{status}:{order_id}")
    if status == OrderStatus.CREATED.value:
        builder.button(text=f"❌Отмена", 
                       callback_data=f"adm_cancel:{order_id}")
    builder.button(text='Назад🔙', callback_data="manager")
    builder.adjust(1)

    return builder.as_markup()


#Админ меню для супер админа
menu_super = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🤖Админы",
                callback_data="list_admins")],
        [InlineKeyboardButton(text="📄Список действий админов",
                callback_data="admins_active")]
    ]
)


#Меню категорий для менеджера
async def kb_menu_categories_by_admin():
    builder = InlineKeyboardBuilder()
    list_ct = await get_categories()

    #Создание кнопок категории из списка
    for but in list_ct:
        builder.button(text=but.name, 
                       callback_data=f'adm_cat:{but.id}')
    
    builder.adjust(2)
    return builder.as_markup()


#Меню товаров в категории для менеджера
async def kb_product_in_cat_by_admin(id: int):
    builder = InlineKeyboardBuilder()
    products = await get_products_in_cat(id)

    for item in products:
        builder.button(text=item.name, 
                       callback_data=f"adm_product:{item.id}")
    
    builder.button(text="🔙 Назад",
                   callback_data="manager")
    builder.adjust(1)
    return builder.as_markup()


#Меню внутри заказа для менеджера
async def kb_in_product_by_admin(product_id: int, is_active: bool):
    builder = InlineKeyboardBuilder()

    if is_active:
        builder.button(text="❌Скрыть", callback_data=f"prod:false:{product_id}")
    else:
        builder.button(text="✅Показать", callback_data=f"prod:true:{product_id}")

    builder.button(text="🔙 Назад",
                   callback_data="manager")

    builder.adjust(1)
    return builder.as_markup()


#Меню изменения админов
delete_or_create_admin = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="✅Добавить", callback_data="add_admin"),
         InlineKeyboardButton(text="❌Удалить", callback_data="del_admin"),],
         [InlineKeyboardButton(text="🔙Назад", callback_data="super")]
    ]
)

#Меню изменения админов
back_super = InlineKeyboardMarkup(
    inline_keyboard=[
         [InlineKeyboardButton(text="🔙Назад", callback_data="super")]
    ]
)