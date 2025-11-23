# api / api.manager.py
from api.endpoints.user_api import UserApi
from api.pet_api import PetApi
from api.store_api import StoreApi
from utils.config import  BASE_URL
import requests

class ApiManager:
    """
    Контейнер для всех API-классов с одной сессией.
    """
    def __init__(self, session: requests.Session):
        self.user_api = UserApi(session=session, base_url=BASE_URL)
        self.store_api = StoreApi(session=session, base_url=BASE_URL)
        self.pet_api = PetApi(session=session, base_url=BASE_URL)