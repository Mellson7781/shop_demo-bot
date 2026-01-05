from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from database.crud.users import get_user_by_id
from database.crud.order import create_order, get_order_user
from database.crud.cart import get_products_in_cart, user_cart
from keyboards.inline.order import kb_orders_confirmation, kb_payment
from states.order import Order


order_rt = Router()


#Обработка начала оформления заказа
@order_rt.callback_query(F.data == "order_start")
async def start_order(query: CallbackQuery, state: FSMContext):
    user_id = query.from_user.id

    user = await get_user_by_id(user_id)
    cart = await user_cart(user_id)

    #Проверка на пустую корзину
    if not cart:
        await query.answer("Корзина пуста 😔", show_alert=True)
        return

    #Проверка на отсутствие username
    if user.username is None:
        await query.answer(
            "Для продолжения офрмления заказа,\n"
            "укажите ваш телеграмм username,\n"
            "что бы мы могли связаться с вами😉!",
            show_alert=True
            )
        return
    
    order_created = await get_order_user(user_id)
    #Проверка на не оплаченые заказы
    if order_created is None:
        await query.answer(
            "У вас есть не оплаченый заказ!\n"
            "Перейдите в '📦 Мои заказы' и оплатите или отмените его.",
            show_alert=True
            )
        return
    
    await state.set_state(Order.confirmation) # Перевод в состояние подтверждения, для блокировки корзины.

    products = await get_products_in_cart(user_id)

    await query.answer("Оформление")
    await query.message.delete()

    text = list()
    c = 0
    total_price = 0
    product_map = {p.id: p for p in products}

    for i in cart:
        product = product_map.get(i.product_id)
        c += 1
        total_price += i.quantity * product.price

        text.append(f"{c}. {product.name}"
                    f" - {i.quantity}шт" 
                    f" - {product.price} руб.")

    text = "\n".join(text)
    text += f"\n\nИтого: {total_price} руб."

    await state.update_data(user_id = user_id,
                      total_price = total_price)

    await query.message.answer(text, 
        reply_markup=kb_orders_confirmation)
    
    


#Продолжение оформление заказа, перевод в состояние оплаты
@order_rt.callback_query(F.data == "order_next")
async def go_to_payment(query: CallbackQuery, state: FSMContext):
    user_id = query.from_user.id
    if await get_order_user(user_id):
        await query.answer("У вас уже есть созданный заказ", show_alert=True)
        return
    
    await query.answer("Оплата")
    data = await state.get_data()

    await create_order(
        user_id=data.get("user_id"),
        total_price=data.get("total_price")
    )

    await state.set_state(Order.payment)


#Продолжение оформление заказа, перевод в состояние оплаты
@order_rt.message(Order.payment)
async def set_state_payment(message: Message, state: FSMContext):
    user_id = message.from_user.id
    order = await get_order_user(user_id)

    await message.edit_text(f"💵Итого: {order.total_price} руб.",
                                  reply_markup= await kb_payment(order.id))
    await state.clear()