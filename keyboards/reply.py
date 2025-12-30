from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🛍 Каталог")],
            [KeyboardButton(text="🛒 Корзина"), KeyboardButton(text="📦 Мои заказы")],
        ],
        resize_keyboard=True
    )