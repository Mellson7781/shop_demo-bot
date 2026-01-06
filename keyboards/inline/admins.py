from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

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
                callback_data="completed")],
    ]
)


#Админ меню для старшего менеджера менеджера
menu_senior = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🛍Категории",
                callback_data="admins_cat")],
        [InlineKeyboardButton(text="🛒Товары",
                callback_data="admins_products")],
        [InlineKeyboardButton(text="💻Заказы",
                callback_data="admins_orders")]
    ]
)


#Админ меню для супер админа
menu_super = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🤖Админы",
                callback_data="admins_cat")],
        [InlineKeyboardButton(text="Список действий админов",
                callback_data="📄admins_products")]
    ]
)