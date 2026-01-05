from aiogram.fsm.state import State, StatesGroup


#Статусы офромления заказа
class Order(StatesGroup):
    confirmation = State()
    payment = State()
