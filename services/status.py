from enum import Enum


class OrderStatus(str, Enum):
    CREATED = "created"
    PAID = "paid"
    CANCELED = "canceled"
    ASSEMBLED = "assembled"
    COMPLEDET = "completed"


class AdminsRole(str, Enum):
    SUPER = "super"
    MANAGER = "manager"