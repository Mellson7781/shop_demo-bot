from aiogram.types import LabeledPrice
from aiogram import Bot
from dotenv import load_dotenv
import os


#Полчение токена оплаты
load_dotenv()
PAY_TOKEN = os.getenv("PAY_TOKEN")


#Отправка инвойса (начало оплаты)
async def send_payment_invoice(
    bot: Bot,
    chat_id: int,
    order_id: int,
    total_price: int
):
    prices = [
        LabeledPrice(
            label="Оплата заказа",
            amount=total_price * 100
        )
    ]

    await bot.send_invoice(
        chat_id=chat_id,
        title="Заказ в магазине",
        description=f"Оплата заказа №{order_id}",
        payload=str(order_id),
        provider_token=PAY_TOKEN,
        currency="RUB",
        prices=prices,
        start_parameter="order-payment"
    )