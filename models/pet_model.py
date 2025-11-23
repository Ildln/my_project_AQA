from typing import Optional, List
from pydantic import BaseModel


class PetModel(BaseModel):
    """Создание модели для валидации данных питомца"""
    id: int
    name: str
    category: Optional[PetCategory]
    photoUrls: List[str]
    tags: Optional[list[PetTags]]
    status: Optional[str]

class PetCategory(BaseModel):
    id: int
    name: str

class PetTags(BaseModel):
    id: int
    name: str