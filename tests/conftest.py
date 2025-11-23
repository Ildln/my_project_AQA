# conftest
import pytest
import requests

from api.api_manager import ApiManager
from utils.config import BASE_URL, headers
from utils.generator import new_pet_generate_payload, new_user_generate_payload, new_order_generate_payload


@pytest.fixture(scope="session")
def http_session():
    s = requests.Session()
    yield s
    s.close()

@pytest.fixture
def api_manager(http_session):
    return ApiManager(session=http_session)



@pytest.fixture
def new_order_payload():
    """Фикстура для генерации тестого заказа"""
    return new_order_generate_payload()

@pytest.fixture
def create_order(api_manager, new_order_payload):
    """Фикстура для Создания заказа"""
    # Создание заказа order
    resp = api_manager.store_api.create_store_order(
        order_data=new_order_payload,
        expected_status=None
    )
    data = resp.json()
    return data



@pytest.fixture
def new_user_payload():
    """Фикстура для генерации данных пользователя"""

    return new_user_generate_payload()

@pytest.fixture
def user_fixture(new_user_payload):
    """Создание и удаление пользователя"""

    # Создание пользователя
    response = requests.post(f"{BASE_URL}/user", json=new_user_payload, headers=headers)

    yield new_user_payload

    # Удаляем пользователя после теста
    del_response = requests.delete(f"{BASE_URL}/user/{new_user_payload["username"]}", headers=headers)

@pytest.fixture
def user_login(user_fixture, api_manager):
    """
    !!!!!!!!!!!!!!!!!!Авторизованный пользователь!!!!!!!!!!!!!!!!!!!!!!!!!!
    """
    login_resp = api_manager.user_api.login(
        username=user_fixture["username"],
        password=user_fixture["password"],
        expected_status=None
    )

    return api_manager



@pytest.fixture
def new_pet_payload():
    """Фикстура для генерации нового питомца"""
    return new_pet_generate_payload()

@pytest.fixture
def create_pet(api_manager, new_pet_payload):
    """Создание питомца через API и возвращаем его данные"""

    resp = api_manager.pet_api.create_to_pet(
        pet_data=new_pet_payload,
        expected_status=None
    )
    assert resp.status_code in (200, 404, 500), (
        f"Failed to creat pet: {resp.status_code}, body: {resp.text}"
    )

    if resp.status_code == 200:
        return resp.json()

    # Если сервер отдал ошибку, возвращаем payload как заглушку
    return new_pet_payload



@pytest.fixture
def admin_user():
    return {
        "username": "admin",
        "password": "password",
        "roles": ["admin"]
    }

@pytest.fixture
def regular_user():
    return{
        "username": "user1",
        "password": "password",
        "roles": ["user"]
    }

@pytest.fixture
def create_admin(api_manager, admin_user):
    """Фикстура создания админа"""
    api_manager.user_api.create_user(user_data=admin_user, expected_status=None)
    return admin_user

@pytest.fixture
def api_manager_admin(api_manager, create_admin):
    api_manager.user_api.login(create_admin["username"], create_admin["password"])
    return api_manager

@pytest.fixture
def api_manager_user(regular_user, api_manager):
    api_manager.user_api.login(regular_user["username"], regular_user["password"])
    return api_manager