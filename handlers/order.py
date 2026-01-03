from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from database.crud import (user_cart, get_product, create_order)
from keyboards.inline import kb_orders_confirmation, kb_orders_payment_conf, kb_payment
from states.order import Order


order_rt = Router()


#Обработка начала оформления заказа
@order_rt.callback_query(F.data == "order_start")
async def start_order(query: CallbackQuery, state: FSMContext):
    user_id = query.from_user.id

    cart_user = await user_cart(user_id)

    await query.answer("Оформление")
    await query.message.delete()

    text = list()
    c = 0
    total_price = 0
    for i in cart_user:
        c += 1
        product = await get_product(i.product_id)
        total_price += i.quantity * product.price

        text.append(f"{c}. {product.name}"
                    f" - {i.quantity}шт" 
                    f" - {product.price} руб.")

    text = "\n".join(text)
    text += f"\n\nИтого: {total_price} руб."

    await query.message.answer(text, 
        reply_markup=kb_orders_confirmation)
    
    await state.update_data(user_id = user_id, 
                            total_price = total_price)


#Продолжение оформление заказа, указание данных о пользователе
@order_rt.callback_query(F.data == "order_next")
async def set_state_name(query: CallbackQuery, state: FSMContext):
    await query.answer("Отлично!")
    await query.message.edit_text("Укажите имя,\nэти данные будут привязаны к заказу!:")

    await state.set_state(Order.name) 


#Обработка состояния ввода имени
@order_rt.message(Order.name)
async def state_name(message: Message, state: FSMContext):
    name = message.text
    
    await state.update_data(name = name)

    await message.answer("Укажите телефон/username,\nэти данные будут привязаны к заказу!:")
    await state.set_state(Order.contact)


#Обработка состояния ввода контакта
@order_rt.message(Order.contact)
async def state_contact(message: Message, state: FSMContext):
    contact = message.text

    await state.update_data(contact = contact)
    data = await state.get_data()

    await message.answer(
        "Проверте все верно?:\n\n"
        f"Имя: {data.get("name")}\n"
        f"Контакт:{data.get("contact")}\n\n"
        f"Итоговая цена: {data.get("total_price")} руб.",
        reply_markup=kb_orders_payment_conf)


#Подтвержденее заказа
@order_rt.callback_query(F.data == "order_payment")
async def payment_def(query: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    order = await create_order(
        user_id=data.get("user_id"),
        name=data.get("name"),
        contact=data.get("contact"),
        total_price=data.get("total_price")
    )

    await query.answer("")
    await query.message.edit_text(f"💵Итого: {data.get("total_price")} руб.",
                                  reply_markup= await kb_payment(order))
    await state.clear()