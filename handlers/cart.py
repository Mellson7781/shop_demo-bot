from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from database.crud.cart import (
    add_in_cart, user_cart, get_products_in_cart,
    cart_minus, cart_plus, cart_product_del, get_cart
)
from database.crud.products import get_product
from keyboards.inline.cart import kb_in_cart_prod, kb_cart_menu
from aiogram.exceptions import TelegramBadRequest

cart_rt = Router()


# ======================
# Проверка FSM
# ======================
async def check_fsm(query: CallbackQuery, state: FSMContext) -> bool:
    if await state.get_state() is not None:
        await query.answer("Вы находитесь на оформлении заказа!", show_alert=True)
        return True
    return False


# ======================
# Отрисовка корзины
# ======================
async def render_cart(user_id: int):
    cart = await user_cart(id=user_id)
    products = await get_products_in_cart(user_id)

    if not cart:
        return "Тут пусто! 😔"

    total_price = 0
    count = 0

    product_map = {p.id: p for p in products}

    for item in cart:
        product = product_map.get(item.product_id)
        if not product or not product.is_active:
            continue
        total_price += product.price * item.quantity
        count += item.quantity

    return f"Итого: {count} товара на {total_price:.2f} ₽:"


# ======================
# Отрисовка продукта
# ======================
async def render_product(cart_id: int) -> dict:
    cart_item = await get_cart(cart_id)
    product = await get_product(cart_item.product_id)

    text = (
        f"💻 Название: {product.name}\n\n"
        f"📄 Описание:\n{product.description}\n\n"
        f"💳 Цена: {product.price} ₽\n\n"
        f"🛒 В корзине: {cart_item.quantity} шт\n\n"
        f"💵 Общая стоимость: {product.price * cart_item.quantity} ₽"
    )

    # Проверяем валидность URL изображения
    image_url = product.image_url if product.image_url else None
    return {"caption": text, "image": image_url, "q": cart_item.quantity}


async def safe_send_photo(query: CallbackQuery, caption: str, image_url: str, reply_markup):
    """
    Безопасная отправка фото: если URL невалидный — отправляем текст.
    """
    if image_url:
        try:
            await query.message.answer_photo(photo=image_url, caption=caption, reply_markup=reply_markup)
            return
        except Exception:
            pass  # Если URL невалидный или недоступен — fallback на текст
    await query.message.answer(text=caption, reply_markup=reply_markup)


# ======================
# Добавление товара
# ======================
@cart_rt.callback_query(F.data.startswith('add_basket:'))
async def add_basket(query: CallbackQuery, state: FSMContext):
    if await check_fsm(query, state):
        return

    product_id = int(query.data.split(':')[1])
    user_id = query.from_user.id

    await add_in_cart(user_id=user_id, product_id=product_id)
    await query.answer("🛒 Товар добавлен в корзину!", show_alert=True)


# ======================
# Открытие корзины
# ======================
@cart_rt.message(F.text == "🛒 Корзина")
async def check_cart(message: Message, state: FSMContext):
    await state.clear()
    user_id = message.from_user.id
    cart_text = await render_cart(user_id)
    await message.answer(cart_text, reply_markup=await kb_cart_menu(user_id))


# ======================
# Просмотр товара из корзины
# ======================
@cart_rt.callback_query(F.data.startswith('cart_pr:'))
async def cart_open_product(query: CallbackQuery, state: FSMContext):
    if await check_fsm(query, state):
        return

    cart_id = int(query.data.split(":")[1])
    result = await render_product(cart_id)

    await query.answer()
    await query.message.delete()

    await safe_send_photo(query, caption=result["caption"], image_url=result["image"],
                          reply_markup=await kb_in_cart_prod(cart_id))


# ======================
# Увеличение количества
# ======================
@cart_rt.callback_query(F.data.startswith('+:'))
async def cart_plus_handler(query: CallbackQuery, state: FSMContext):
    if await check_fsm(query, state):
        return

    cart_id = int(query.data.split(":")[1])
    await cart_plus(cart_id)
    result = await render_product(cart_id)

    await query.answer()
    try:
        await query.message.edit_caption(caption=result["caption"],
                                        reply_markup=await kb_in_cart_prod(cart_id))
    except TelegramBadRequest:
        await query.message.edit_text(text=result["caption"],
                                      reply_markup=await kb_in_cart_prod(cart_id))



# ======================
# Уменьшение количества
# ======================
@cart_rt.callback_query(F.data.startswith('-:'))
async def cart_minus_handler(query: CallbackQuery, state: FSMContext):
    if await check_fsm(query, state):
        return

    cart_id = int(query.data.split(":")[1])
    user_id = query.from_user.id

    await cart_minus(cart_id)
    result = await render_product(cart_id)

    await query.answer()
    if result["q"] < 1:
        await cart_product_del(cart_id)
        await query.message.delete()
        cart_text = await render_cart(user_id)
        await query.message.answer(cart_text, reply_markup=await kb_cart_menu(user_id))
    else:
        try:
            await query.message.edit_caption(caption=result["caption"],
                                            reply_markup=await kb_in_cart_prod(cart_id))
        except TelegramBadRequest:
            await query.message.edit_text(text=result["caption"],
                                      reply_markup=await kb_in_cart_prod(cart_id))


# ======================
# Удаление товара
# ======================
@cart_rt.callback_query(F.data.startswith('delete_pr:'))
async def cart_delete_handler(query: CallbackQuery, state: FSMContext):
    if await check_fsm(query, state):
        return

    cart_id = int(query.data.split(":")[1])
    user_id = query.from_user.id

    await cart_product_del(cart_id)
    await query.message.delete()

    cart_text = await render_cart(user_id)
    await query.message.answer(cart_text, reply_markup=await kb_cart_menu(user_id))


# ======================
# Назад к корзине
# ======================
@cart_rt.callback_query(F.data == 'cart')
async def cart_back_handler(query: CallbackQuery, state: FSMContext):
    await query.answer()
    await query.message.delete()
    await state.clear()

    user_id = query.from_user.id
    cart_text = await render_cart(user_id)
    await query.message.answer(cart_text, reply_markup=await kb_cart_menu(user_id))