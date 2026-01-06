from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

#Кнопка обновления данных
button_update = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="⚙️Обновить информацию",
                  callback_data=f"update_info")]
])