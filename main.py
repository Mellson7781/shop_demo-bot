from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
import asyncio, os


#Загрузка из .env
load_dotenv()


#Получение токина бота и url бд из .env 
BOT_TOKEN = os.getenv("BOT_TOKEN") 


# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


#Функция для запуска бота
async def main():
    #Удаляем все накполеные обращения при запуске
    await bot.delete_webhook(drop_pending_updates=True)
    #Подключение роутеров
    #dp.include_routers()
    #Запуск polling (Проще говоря запуск бота)
    await dp.start_polling(bot)


#Точка входа
if __name__ == "__main__":
    asyncio.run(main())