from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.exceptions import TelegramBadRequest

from database.crud.admins import (
    get_is_admin,
    status_get_order,
    get_order,
    get_order_items,
    get_user_by_order_id,
    update_order_status,
    get_product,
    update_product_status
)

from keyboards.inline.admins import (
    menu_manager,
    button_back,
    kb_list_of_orders,
    kb_status,
    kb_menu_categories_by_admin,
    kb_product_in_cat_by_admin,
    kb_in_product_by_admin
)

from services.status import OrderStatus
from middlewares.admin_check import AdminMiddleware
from middlewares.admin_logger import AdminLoggerMiddleware


manager_rt = Router()


manager_rt.callback_query.middleware(AdminMiddleware())
manager_rt.callback_query.middleware(AdminLoggerMiddleware())
manager_rt.message.middleware(AdminLoggerMiddleware())


# =======================
# Расшифровка статусов
# =======================
STATUS = {
    OrderStatus.CREATED.value: "Создано",
    OrderStatus.PAID.value: "Оплачено",
    OrderStatus.CANCELED.value: "Отменён",
    OrderStatus.ASSEMBLED.value: "В сборке",
    OrderStatus.COMPLEDET.value: "Завершён",
}


# =======================
# Вспомогательные функции
# =======================
def build_items_text(items) -> str:
    return "\n".join(
        f"• {item.product_name} — {item.quantity} шт. × {item.price} ₽"
        for item in items
    )


def get_next_status(current_status: str) -> str:
    flow = [
        OrderStatus.PAID.value,
        OrderStatus.ASSEMBLED.value,
        OrderStatus.COMPLEDET.value,
    ]

    if current_status not in flow:
        return current_status

    index = flow.index(current_status)
    if index == len(flow) - 1:
        return current_status

    return flow[index + 1]


async def show_orders(query: CallbackQuery, status: OrderStatus, title: str, empty_text: str):
    orders = await status_get_order(status.value)

    if not orders:
        await query.message.edit_text(empty_text, reply_markup=button_back)
        return

    orders_id = sorted(order.id for order in orders)

    await query.message.edit_text(
        title,
        reply_markup=await kb_list_of_orders(orders_id, status.value),
    )


async def show_product(query: CallbackQuery, product_id):
    products = await get_product(id=product_id)

    if not products:
        await query.answer("Не удалось получить информацию о заказе!")
        return
    try:
        await query.message.answer_photo(
            products.image_url,
            caption=f"💻Название: {products.name}\n\n"
            f"📄Описание:\n{products.description}\n\n"
            f"💳 Цена: {products.price}🏷 Руб",
            reply_markup = await kb_in_product_by_admin(product_id, products.is_active))
    except TelegramBadRequest:      
        await query.message.answer(text=
            f"💻Название: {products.name}\n\n"
            f"📄Описание:\n{products.description}\n\n"
            f"💳 Цена: {products.price}🏷 Руб",
            reply_markup = await kb_in_product_by_admin(product_id, products.is_active))


# =======================
# Меню менеджера
# =======================
@manager_rt.callback_query(F.data == "manager")
async def back_manager(query: CallbackQuery):
    await query.answer("Вы вернулись назад")
    await query.message.delete()
    await query.message.answer(
        "🗃 Выберите категорию заказа",
        reply_markup=menu_manager,
    )


# =======================
# Списки заказов
# =======================
@manager_rt.callback_query(F.data == "created")
async def manager_created(query: CallbackQuery):
    await show_orders(
        query,
        OrderStatus.CREATED,
        "🛒 Новые заказы:",
        "⚠️ Новых заказов нет!",
    )


@manager_rt.callback_query(F.data == "paid")
async def manager_paid(query: CallbackQuery):
    await show_orders(
        query,
        OrderStatus.PAID,
        "💰 Оплаченные заказы:",
        "⚠️ Оплаченных заказов нет!",
    )


@manager_rt.callback_query(F.data == "assembled")
async def manager_assembled(query: CallbackQuery):
    await show_orders(
        query,
        OrderStatus.ASSEMBLED,
        "✅ Активные заказы:",
        "⚠️ Активных заказов нет!",
    )


@manager_rt.callback_query(F.data == "adm_completed")
async def manager_completed(query: CallbackQuery):
    await show_orders(
        query,
        OrderStatus.COMPLEDET,
        "🗂 Завершённые заказы:",
        "⚠️ Завершённых заказов нет!",
    )


# =======================
# Информация о заказе
# =======================
@manager_rt.callback_query(F.data.startswith("order_adm:"))
async def info_order(query: CallbackQuery):
    _, status, order_id = query.data.split(":")
    order_id = int(order_id)

    order = await get_order(order_id)
    if not order:
        await query.answer("Заказ не найден", show_alert=True)
        return

    items = await get_order_items(order_id)
    user = await get_user_by_order_id(order_id)

    items_text = build_items_text(items)

    await query.message.edit_text(
        text=(
            f"👤 Пользователь: @{user.username}\n"
            f"🆔 ID: {user.id}\n\n"
            f"📄 Заказ №{order.id}\n"
            f"📌 Статус: {STATUS.get(order.status)}\n\n"
            f"📦 Товары:\n{items_text}\n\n"
            f"💰 Сумма: {order.total_price} ₽\n"
            f"📆 Создан: {order.created_at}"
        ),
        reply_markup = await kb_status(order_id, status),
    )


# =======================
# Перевод в следующий статус
# =======================
@manager_rt.callback_query(F.data.startswith("next:"))
async def status_next(query: CallbackQuery):
    _, current_status, order_id = query.data.split(":")
    order_id = int(order_id)

    order = await get_order(order_id)
    if not order:
        await query.answer("Заказ не найден", show_alert=True)
        return

    items = await get_order_items(order_id)
    user = await get_user_by_order_id(order_id)

    next_status = get_next_status(current_status)

    if next_status != current_status:
        result = await update_order_status(order_id, next_status)

        if not result:
            await query.answer("Не удалось обновить информацию о заказе!")
            return
        await query.bot.send_message(
            chat_id=user.id,
            text=f"🔜Статус заказа №{order.id} - Обновлен на: {STATUS.get(next_status)}"
        )


    items_text = build_items_text(items)

    await query.message.edit_text(
        text=(
            f"👤 Пользователь: @{user.username}\n"
            f"🆔 ID: {user.id}\n\n"
            f"📄 Заказ №{order.id}\n"
            f"📌 Статус: {STATUS.get(next_status)}\n\n"
            f"📦 Товары:\n{items_text}\n\n"
            f"💰 Сумма: {order.total_price} ₽\n"
            f"📆 Создан: {order.created_at}"
        ),
        reply_markup= await kb_status(order_id, next_status),
    )

    await query.answer("Статус обновлён ✅")


# =======================
#Отмена заказа
# =======================
@manager_rt.callback_query(F.data.startswith("adm_cancel:"))
async def status_cancal(query: CallbackQuery):
    _, order_id = query.data.split(":")
    order_id = int(order_id)

    order = await get_order(order_id)
    if not order:
        await query.answer("Заказ не найден", show_alert=True)
        return

    user = await get_user_by_order_id(order_id)


    result = await update_order_status(order_id, OrderStatus.CANCELED.value)

    if not result:
        await query.answer("Не удалось обновить информацию о заказе!")
        return
    await query.bot.send_message(
        chat_id=user.id,
        text=f"🔜Заказ №{order.id} - ❌Отменен"
        )

    await query.answer("❌Заказ отменен!", show_alert=True)
    await query.message.delete()


# =======================
#Обработка действий кнопки "Товары"
# =======================
@manager_rt.callback_query(F.data.startswith("admins_products"))
async def status_cancal(query: CallbackQuery):
    await query.answer("Вы зашли в католог!")
    await query.message.edit_text('⚙️Выберите категорию:', 
                   reply_markup= await kb_menu_categories_by_admin())
    

#Получение товаров из выбраной категории
@manager_rt.callback_query(F.data.startswith('adm_cat:'))
async def products_in_cat(query: CallbackQuery):
    await query.answer("Вы зашли в категорию!")
    await query.message.delete()

    cat_id = int(query.data.split(':')[1])
    await query.message.answer("⚙️Доступные товары:",
            reply_markup = await kb_product_in_cat_by_admin(cat_id))


#Получение карточки товара
@manager_rt.callback_query(F.data.startswith('adm_product:'))
async def product_info(query: CallbackQuery):
    await query.answer("Вы смотрите карточку товара!")
    await query.message.delete()

    product_id = int(query.data.split(':')[1])

    await show_product(query, product_id)


#Скрыть\показать товар
@manager_rt.callback_query(F.data.startswith('prod:'))
async def product_info(query: CallbackQuery):
    await query.answer("Вы смотрите карточку товара!")
    await query.message.delete()

    _, result, product_id = query.data.split(':')
    product_id = int(product_id)

    if result == "false":
        result = False
    else:
        result = True
    
    result = await update_product_status(product_id, result)
    if not result:
        query.answer("Не удалось скрыть/показать товар!",
                     show_alert=True)
        return

    await show_product(query, product_id)