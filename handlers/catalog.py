from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from keyboards.inline import kb_menu_categories, menu_add_basket, menu_back
from database.crud import get_products_in_cat


#Роутер католога 
catalog_rt = Router()


@catalog_rt.message(F.text == "🛍 Каталог")
async def get_categories(message: Message):
    await message.answer('🗂Выберите категорию:', 
                   reply_markup= await kb_menu_categories())
    

#Получение товаров из выбраной категории
@catalog_rt.callback_query(F.data.startswith('cat_'))
async def products_in_cat(query: CallbackQuery):
    await query.answer("Вы зашли в категорию!")
    await query.message.delete()

    cat_id = int(query.data.split('_')[1])
    products = await get_products_in_cat(id=cat_id)

    for item in products:
        await query.message.answer_photo(
            FSInputFile(item.image_url),
            caption=f"💻Название: {item.name}\n\n"
            f"📄Описание:\n{item.description}\n\n"
            f"💳 Цена: {item.price}🏷 Руб",
            reply_markup=menu_add_basket) 

    await query.message.answer("📌 Вернуться", reply_markup= await menu_back('cat'))


@catalog_rt.callback_query(F.data == 'back_cat')
async def get_categories(query: CallbackQuery):
    await query.answer("Вы вернулись назад")
    await query.message.delete()
    await query.message.answer('🗂Выберите категорию:', 
                   reply_markup= await kb_menu_categories())