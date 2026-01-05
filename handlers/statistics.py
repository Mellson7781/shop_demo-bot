from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from database.crud.order import (get_order_user, order_status_canel,
                                 get_order)
from database.crud.statistics import status_get_order, get_order_items
from keyboards.inline.statistics import (
    kb_filter_my_order, back_menu_my_orders,
    kb_list_of_orders
    )
from keyboards.inline.order import kb_payment
from services.status import OrderStatus


statistics_rt = Router()


#Расшифровка статусов
STATUS = {
        OrderStatus.CREATED.value: "Создано",
        OrderStatus.PAID.value: "Оплачено",
        OrderStatus.CANCELED.value: "Отменён",
        OrderStatus.ASSEMBLED.value: "В сборке" ,
        OrderStatus.COMPLEDET.value: "Завершенный"
    }


#Посмотреть заказаы пользователя 
@statistics_rt.message(F.text == "📦 Мои заказы")
async def get_my_orders(message: Message):
    await message.answer(
        "📦 Какой категории хотите посмотреть заказы:",
        reply_markup=kb_filter_my_order
    )


#Кнопка назад 
@statistics_rt.callback_query(F.data == "my_orders")
async def get_my_orders(qeury: CallbackQuery):
    await qeury.answer("Вы вернулись назад!")
    await qeury.message.delete()
    await qeury.message.answer(
        "📦 Какой категории хотите посмотреть заказы:",
        reply_markup=kb_filter_my_order
    )


#Посмотреть не оплаченый заказ
@statistics_rt.callback_query(F.data == "for_payment")
async def for_payment_def(query: CallbackQuery):
    await query.answer("Не оплаченый заказ")

    user_id = query.from_user.id
    order = await get_order_user(user_id)

    if order is None:
        await query.message.edit_text(
            "🕊Не оплаченных заказов нет!",
            reply_markup=back_menu_my_orders
        )
        return
    
    order_items = await get_order_items(order.id)

    text = list()
    for item in order_items:
        text.append(f"{item.product_name} - в количестве {item.quantity}" 
        f" шт. Цена: {item.price} руб.\n")
    text = "\n".join(text)

    await query.message.delete()
    await query.message.answer(text=
        f"📄Заказ №{order.id} - Статус: {STATUS.get(order.status)}\n"
        f"📂Список товаров:\n{text}\n"
        f"💰На сумму: {order.total_price} руб.\n\n"
        f"📆Созданным: {order.created_at}",
        reply_markup=await kb_payment(order.id)
    )


#Отменить оплату
@statistics_rt.callback_query(F.data.startswith("cancel:"))
async def cancel_payment(query: CallbackQuery):
    user_id = query.from_user.id
    order_id = int(query.data.split(":")[1])

    if await get_order_user(user_id) is None:
        query.answer("Этого заказа уже нет!",
                     show_alert=True)
        return
    
    await order_status_canel(order_id)
    await query.answer("Оплата заказа отменена!",
                       show_alert=True)


#Посмотреть не завершенные заказы
@statistics_rt.callback_query(F.data == "not_completed")
async def not_completed(query: CallbackQuery):
    await query.answer("Не завершенные заказы")
    user_id = query.from_user.id

    orders_paid = await status_get_order(user_id, OrderStatus.PAID.value)
    orders_assembled = await status_get_order(user_id, OrderStatus.ASSEMBLED.value)
    orders = orders_paid + orders_assembled

    if not orders:
        await query.message.answer("😉Не завершенных заказов нет!",
                                   reply_markup=back_menu_my_orders
                                    )
        return 
    
    orders_id = sorted(i.id for i in orders)

    await query.message.edit_text("❌Не завершенные заказы:",
                reply_markup = await kb_list_of_orders(orders_id))


#Посмотреть завершенные заказы
@statistics_rt.callback_query(F.data == "completed")
async def completed(query: CallbackQuery):
    await query.answer("Завершенные заказы")
    user_id = query.from_user.id
    orders = await status_get_order(user_id, OrderStatus.COMPLEDET.value)

    if not orders:
        await query.message.edit_text("⚠️Завершенных заказов нет!",
                                   reply_markup=back_menu_my_orders
                                    )
        return 
    
    orders_id = sorted(i.id for i in orders)

    await query.message.edit_text("✅Завершенные заказы:",
                reply_markup = await kb_list_of_orders(orders_id))


#Посмотреть информацию о заказе
@statistics_rt.callback_query(F.data.startswith("order:"))
async def info_order(query: CallbackQuery):
    order_id = int(query.data.split(":")[1])
    order = await get_order(order_id)

    if order is None:
        await query.answer("К сожелению,\n"
        "мы не можем получить информацию"
        "по этому заказу🥺",
        show_alert=True
        )
        return
    
    order_items = await get_order_items(order_id)

    if not order_items:
        await query.answer("К сожелению,\n"
        "мы не можем получить информацию"
        "по этому заказу🥺",
        show_alert=True
        )
        return
    
    text = list()
    for item in order_items:
        text.append(f"{item.product_name} - в количестве {item.quantity}" 
        f" шт. Цена: {item.price} руб.\n")
    text = "\n".join(text)

    await query.answer(f"Заказ №{order_id}")
    await query.message.delete()
    await query.message.answer(text=
        f"📄Заказ №{order.id} - Статус: {STATUS.get(order.status)}\n"
        f"📂Список товаров:\n\n{text}\n"
        f"💰На сумму: {order.total_price} руб.\n\n"
        f"📆Созданным: {order.created_at}",
        reply_markup=back_menu_my_orders
    )

