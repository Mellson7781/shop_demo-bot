from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from keyboards.inline.catalog import (kb_menu_categories, 
                              kb_in_product, 
                              kb_product_in_cat)
from database.crud.products import get_product


#Роутер католога 
catalog_rt = Router()


#Католог:
@catalog_rt.message(F.text == "🛍 Каталог")
async def get_categories(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('🗂Выберите категорию:', 
                   reply_markup= await kb_menu_categories())


@catalog_rt.callback_query(F.data == "catalog")
async def get_categories(query: CallbackQuery):
    await query.answer("Вы зашли в католог!")
    await query.message.edit_text('🗂Выберите категорию:', 
                   reply_markup= await kb_menu_categories())
#

#Получение товаров из выбраной категории
@catalog_rt.callback_query(F.data.startswith('cat_'))
async def products_in_cat(query: CallbackQuery):
    await query.answer("Вы зашли в категорию!")
    await query.message.delete()

    cat_id = int(query.data.split('_')[1])
    await query.message.answer("📌 Доступные товары🛒:",
            reply_markup = await kb_product_in_cat(cat_id))

   


#Получение карточки товара
@catalog_rt.callback_query(F.data.startswith('product_'))
async def product_info(query: CallbackQuery):
    await query.answer("Вы смотрите карточку товара!")
    await query.message.delete()

    product_id = int(query.data.split('_')[1])
    products = await get_product(id=product_id)

    if products.is_active:
        await query.message.answer_photo(
            FSInputFile(products.image_url),
            caption=f"💻Название: {products.name}\n\n"
            f"📄Описание:\n{products.description}\n\n"
            f"💳 Цена: {products.price}🏷 Руб",
            reply_markup = await kb_in_product(id=products.id))


#Кнопка назад
@catalog_rt.callback_query(F.data == 'back_cat')
async def get_categories(query: CallbackQuery):
    await query.answer("Вы вернулись назад")
    await query.message.delete()
    await query.message.answer('🗂Выберите категорию:', 
                   reply_markup= await kb_menu_categories())