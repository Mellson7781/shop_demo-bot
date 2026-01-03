from aiogram.fsm.state import State, StatesGroup


#Статусы офромления заказа
class Order(StatesGroup):
    name = State()
    contact = State()
    waypayment = State()
    createorder = State()
    payment = State()
