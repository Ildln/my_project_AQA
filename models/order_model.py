from pydantic import BaseModel


class OrderModel(BaseModel):
    """Создаем модель для валидации данных заказа"""
    id: int
    petId: int
    quantity: int
    shipDate: str
    status: str
    complete: bool