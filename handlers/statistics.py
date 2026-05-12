from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from database.crud.order import get_order_user, order_status_cancel, get_order
from database.crud.statistics import status_get_order, get_order_items
from keyboards.inline.statistics import kb_filter_my_order, back_menu_my_orders, kb_list_of_orders
from keyboards.inline.order import kb_payment
from services.status import OrderStatus
from aiogram.exceptions import TelegramBadRequest

statistics_rt = Router()

# =======================
# Расшифровка статусов
# =======================
STATUS = {
    OrderStatus.CREATED.value: "Создано",
    OrderStatus.PAID.value: "Оплачено",
    OrderStatus.CANCELED.value: "Отменён",
    OrderStatus.ASSEMBLED.value: "В сборке",
    OrderStatus.COMPLEDET.value: "Завершён"
}

# =======================
# Вспомогательная функция
# =======================
def build_order_text(order, items) -> str:
    items_text = "\n".join(
        f"{item.product_name} - {item.quantity} шт. | Цена: {item.price} руб."
        for item in items
    )
    return (
        f"📄 Заказ №{order.id} - Статус: {STATUS.get(order.status)}\n"
        f"📂 Список товаров:\n{items_text}\n"
        f"💰 На сумму: {order.total_price} руб.\n"
        f"📆 Создан: {order.created_at}"
    )

async def safe_edit_message(message, **kwargs):
    try:
        await message.edit_text(**kwargs)
    except TelegramBadRequest:
        await message.answer(**kwargs)

async def safe_delete_message(message):
    try:
        await message.delete()
    except TelegramBadRequest:
        pass

# =======================
# Мои заказы
# =======================
@statistics_rt.message(F.text == "📦 Мои заказы")
async def get_my_orders(message: Message):
    await message.answer(
        "📦 Какой категории хотите посмотреть заказы:",
        reply_markup=kb_filter_my_order
    )

# Кнопка назад
@statistics_rt.callback_query(F.data == "my_orders")
async def get_my_orders_cb(query: CallbackQuery):
    await query.answer("Вы вернулись назад!")
    await safe_delete_message(query.message)
    await query.message.answer(
        "📦 Какой категории хотите посмотреть заказы:",
        reply_markup=kb_filter_my_order
    )

# Не оплаченные заказы
@statistics_rt.callback_query(F.data == "for_payment")
async def for_payment_def(query: CallbackQuery):
    await query.answer("Неоплаченные заказы")
    user_id = query.from_user.id
    order = await get_order_user(user_id)
    if not order:
        await safe_edit_message(query.message,
            text="🕊 Неоплаченных заказов нет!",
            reply_markup=back_menu_my_orders
        )
        return

    order_items = await get_order_items(order.id)
    text = build_order_text(order, order_items)
    await safe_delete_message(query.message)
    await query.message.answer(text=text, reply_markup=await kb_payment(order.id))

# Отмена заказа
@statistics_rt.callback_query(F.data.startswith("cancel:"))
async def cancel_payment(query: CallbackQuery):
    user_id = query.from_user.id
    order_id = int(query.data.split(":")[1])
    order = await get_order_user(user_id)
    if not order:
        await query.answer("Этого заказа уже нет!", show_alert=True)
        return

    if order.status == OrderStatus.CANCELED.value:
        await query.answer("Этот заказ уже отменен!", show_alert=True)
        return

    await order_status_cancel(order_id)
    await query.answer("Оплата заказа отменена!", show_alert=True)
    await query.message.delete()

# Не завершенные заказы
@statistics_rt.callback_query(F.data == "not_completed")
async def not_completed(query: CallbackQuery):
    await query.answer("Не завершенные заказы")
    user_id = query.from_user.id
    orders_paid = await status_get_order(user_id, OrderStatus.PAID.value)
    orders_assembled = await status_get_order(user_id, OrderStatus.ASSEMBLED.value)
    orders = orders_paid + orders_assembled
    if not orders:
        await safe_edit_message(query.message, text="😉 Не завершенных заказов нет!", reply_markup=back_menu_my_orders)
        return

    orders_id = sorted(o.id for o in orders)
    await safe_edit_message(query.message, text="❌ Не завершенные заказы:", reply_markup=await kb_list_of_orders(orders_id))

# Завершенные заказы
@statistics_rt.callback_query(F.data == "completed")
async def completed(query: CallbackQuery):
    await query.answer("Завершенные заказы")
    user_id = query.from_user.id
    orders = await status_get_order(user_id, OrderStatus.COMPLEDET.value)
    if not orders:
        await safe_edit_message(query.message, text="⚠️ Завершенных заказов нет!", reply_markup=back_menu_my_orders)
        return

    orders_id = sorted(o.id for o in orders)
    await safe_edit_message(query.message, text="✅ Завершенные заказы:", reply_markup=await kb_list_of_orders(orders_id))

# Информация о заказе
@statistics_rt.callback_query(F.data.startswith("order:"))
async def info_order(query: CallbackQuery):
    order_id = int(query.data.split(":")[1])
    order = await get_order(order_id)
    if not order:
        await query.answer("К сожалению, мы не можем получить информацию по этому заказу 🥺", show_alert=True)
        return

    order_items = await get_order_items(order_id)
    if not order_items:
        await query.answer("К сожалению, мы не можем получить информацию по этому заказу 🥺", show_alert=True)
        return

    text = build_order_text(order, order_items)
    await query.answer(f"Заказ №{order_id}")
    await safe_delete_message(query.message)
    await query.message.answer(text=text, reply_markup=back_menu_my_orders)