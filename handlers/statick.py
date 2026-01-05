from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from database.crud.statick import get_orders
from keyboards.inline_all import kb_filter_my_order


statick_rt = Router()


@statick_rt.message(F.text == "📦 Мои заказы")
async def get_my_orders(message: Message):
    await message.answer(
        "📦 Какой категории хотите посмотреть заказы:",
        reply_markup=kb_filter_my_order
    )


@statick_rt.callback_query(F.data == "completed")
async def get_completed_orders(query: CallbackQuery):
    user_id = query.from_user.id
    orders = await get_orders(user_id)

    text = ""
    for i in orders:
        if i.status == "compl":
            text += f"Заказ №{i.id}, статус: Выполнен\n"

    if not text:
        text = "✅ Выполненных заказов нет"

    await query.answer()
    await query.message.answer(text)


@statick_rt.callback_query(F.data == "not_completed")
async def get_not_completed_orders(query: CallbackQuery):
    user_id = query.from_user.id
    orders = await get_orders(user_id)

    STATUS = {
        "paid": "Оплачено",
        "cancel": "Отменён",
    }

    text = ""
    for i in orders:
        if i.status != "compl":
            text += f"Заказ №{i.id}, статус: {STATUS.get(i.status, i.status)}\n"

    if not text:
        text = "📦 Невыполненных заказов нет"

    await query.answer()
    await query.message.answer(text)