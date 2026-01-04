from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from database.crud import (add_in_cart, user_cart, 
                           get_product, cart_minus,
                           get_cart, cart_plus, 
                           cart_product_del)
from keyboards.inline import kb_in_cart_prod, kb_cart_menu
from states.order import Order


catr_rt = Router()


#Отрисовка меню корзины
async def render_cart(user_id: int):
    cart = await user_cart(id=user_id)

    count = 0
    total_price = 0

    for i in cart:
        product = await get_product(i.product_id)
        count += i.quantity
        total_price += product.price * i.quantity

    if count == 0:
        return "Тут пусто! 😔"
    
    return f"Итого: {count} товара на {total_price} ₽:"


#Отрисовка карточки товара в корзине
async def render_product(cart_id: int) -> dict:
    cart_item = await get_cart(cart_id)
    product = await get_product(cart_item.product_id)
    
    text = (
    f"💻Название: {product.name}\n\n"
    f"📄Описание:\n{product.description}\n\n"
    f"💳 Цена: {product.price}🏷 Руб\n\n"
    f"🛒В корзине: {cart_item.quantity} шт\n\n"
    f"💵 Общая стоимость: {product.price*cart_item.quantity} Руб")

    return {"caption":text, "image": product.image_url, "q": cart_item.quantity}



#Обработка add_basket
@catr_rt.callback_query(F.data.startswith('add_basket:'))
async def add_basket(query: CallbackQuery, state: FSMContext):
    if await state.get_state() is not None:
        await query.answer("Вы находитесь на офрмление заказа!",
                       show_alert=True)
        return

    product_id = int(query.data.split(':')[1])
    user_id = query.from_user.id

    await add_in_cart(user_id=user_id, 
                      product_id=product_id)
    

    await query.answer("🛒Товар добавлен в корзину!",
                       show_alert=True)


#Обработка кнопки "🛒 Корзина"
@catr_rt.message(F.text == "🛒 Корзина")
async def check_cart(message: Message, state: FSMContext):
    await state.clear()
    user_id = message.from_user.id
    cart = await render_cart(user_id)

    await message.answer(cart,
        reply_markup = await kb_cart_menu(user_id))


#Получение карточки товара в корзине
@catr_rt.callback_query(F.data.startswith('cart_pr:'))
async def product_in_cart(query: CallbackQuery, state: FSMContext):
    if await state.get_state() is not None:
        await query.answer("Вы находитесь на офрмление заказа!",
                       show_alert=True)
        return
    
    cart_id = int(query.data.split(":")[1])
    result = await render_product(cart_id)

    await query.answer("")
    await query.message.delete()
    await query.message.answer_photo(FSInputFile(result["image"]),
            caption = result["caption"],
            reply_markup= await kb_in_cart_prod(cart_id))
    

#Добавление товара
@catr_rt.callback_query(F.data.startswith('+:'))
async def product_in_cart(query: CallbackQuery, state: FSMContext):
    if await state.get_state() is not None:
        await query.answer("Вы находитесь на офрмление заказа!",
                       show_alert=True)
        return
    cart_id = int(query.data.split(":")[1])
    await cart_plus(cart_id)

    result = await render_product(cart_id)

    await query.answer("")
    await query.message.edit_caption(caption = result["caption"],
            reply_markup= await kb_in_cart_prod(cart_id))


#Убавление товара
@catr_rt.callback_query(F.data.startswith('-:'))
async def product_in_cart(query: CallbackQuery, state: FSMContext):
    if await state.get_state() is not None:
        await query.answer("Вы находитесь на офрмление заказа!",
                       show_alert=True)
        return
    cart_id = int(query.data.split(":")[1])
    id = query.from_user.id

    await cart_minus(cart_id)

    cart = await render_cart(id)
    result = await render_product(cart_id)

    await query.answer("")

    if result["q"] > 0:
        await query.answer("")
        await query.message.edit_caption(caption = result["caption"],
        reply_markup= await kb_in_cart_prod(cart_id))
        return
    
    await query.message.delete()
    await cart_product_del(cart_id)
    await query.message.answer(cart,
        reply_markup= await kb_cart_menu(id))
    


#Удаление товара
@catr_rt.callback_query(F.data.startswith('delete_pr:'))
async def product_in_cart(query: CallbackQuery, state: FSMContext):
    if await state.get_state() is not None:
        await query.answer("Вы находитесь на офрмление заказа!",
                       show_alert=True)
        return
    cart_id = int(query.data.split(":")[1])
    await cart_product_del(cart_id)

    await query.answer("")
    await query.message.delete()

    user_id = query.from_user.id

    cart = await render_cart(user_id)
    await query.message.answer(cart,
                        reply_markup = await kb_cart_menu(user_id))
    

#Назад к корзине
@catr_rt.callback_query(F.data == 'cart')
async def product_in_cart(query: CallbackQuery, state: FSMContext):
    await query.answer("")
    await query.message.delete()

    await state.clear()

    user_id = query.from_user.id
   
    cart = await render_cart(user_id)
    await query.message.answer(cart,
                        reply_markup = await kb_cart_menu(user_id))