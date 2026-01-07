from aiogram import Bot, Router, F
from aiogram.types import PreCheckoutQuery, CallbackQuery, Message
from services.payment import send_payment_invoice
from database.crud.order import order_status_paid, get_order
from services.status import OrderStatus


payment_rt = Router()


#Вызов функции send_payment_invoice
@payment_rt.callback_query(F.data.startswith("payment:"))
async def send_invoice(query: CallbackQuery, bot: Bot):
    await query.answer("Проведение опллаты")
    await query.message.delete()
    
    order_id = int(query.data.split(":")[1])
    order = await get_order(order_id)
    total_price = order.total_price

    if order.status != OrderStatus.CREATED.value:
        await query.answer("Этот заказ уже нельзя оплатить!",
                           show_alert=True)
        return
    await send_payment_invoice(
        bot, query.message.chat.id, 
        order_id=order_id,
        total_price=total_price
    )


#Подтверждение оплаты
@payment_rt.pre_checkout_query()
async def process_pre_checkout(pre_checkout: PreCheckoutQuery):
    await pre_checkout.answer(ok=True)


#Положительный ответ платежной системы
@payment_rt.message(F.successful_payment)
async def successful_payment_handler(message: Message):
    if message.successful_payment:
        order_id = int(message.successful_payment.invoice_payload)
        payment_id = message.successful_payment.telegram_payment_charge_id

        await order_status_paid(order_id, payment_id)

        await message.answer(
            f"✅ Заказ №{order_id} успешно оплачен!"
        )