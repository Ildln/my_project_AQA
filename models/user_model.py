from pydantic import BaseModel


class UserModel(BaseModel):
    """Создаем модель для теста на регистрацию пользователя. creat_user"""
    id: int
    username: str
    firstName: str
    lastName: str
    email: str
    password: str
    phone: str
    userStatus: int