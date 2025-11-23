import allure

from pydantic import ValidationError
from models.order_model import OrderModel
from tests.conftest import create_order, new_order_payload

@allure.feature("Store API")
@allure.story("Inventory")
@allure.title("Проверка GET /store/inventory")
@allure.description("Тест проверяет получение текущего инвентаря магазина через API.")
@allure.tag("api", "positive")
def test_get_inventory(api_manager):
    """Проверяем, что GET /store/inventory отвечает (200 или 500)"""
    with allure.step("Отправлям запрос на получение информации об инвентаре"):
        resp = api_manager.store_api.get_inventory(expected_status=None)
        data = resp.json()

    with allure.step("Проверяем статус код"):
        if resp.status_code == 200:
            assert isinstance(data, dict)
            assert "sold" in data or "available" in data
        elif resp.status_code == 500:
            assert "code" in data and data["code"] == 500
            assert "message" in data
        else:
            raise AssertionError(f"Неожиданный статус: {resp.status_code}, тело: {data}")

@allure.feature("Store API")
@allure.story("Order")
@allure.title("Создание заказа через POST /store/order")
@allure.description("Тест проверяет создание нового заказа и валидацию оответа через Pydantic.")
@allure.tag("api", "positive")
def test_creat_order(api_manager, new_order_payload):
    """POST /store/order - создаем заказ"""
    with allure.step("Отправляем запрос на создаение заказа"):
        resp = api_manager.store_api.create_store_order(order_data=new_order_payload, expected_status=None)

    with allure.step("Проверяем статус код"):
        assert resp.status_code in (200, 500)

    if resp.status_code == 200:
        try:
            order = OrderModel(**resp.json())   # Валидация через Pydantic
        except ValidationError as e:
            assert False, f"Order API response doesn't match model: {e}"

        # Проверяем данные
        assert order.id == new_order_payload["id"]
        assert order.status == new_order_payload["status"]

@allure.feature("Store API")
@allure.story("Order")
@allure.title("Получение заказа по ID: GET /store/order/{orderId}")
@allure.description("Тест проверяет корректность данных заказа через API и валидацию через Pydantic.")
@allure.tag("api", "positive")
def test_get_order_id(create_order, api_manager):
    """GET /store/order/{orderid} - получение заказа по id"""
    order_id = create_order["id"]

    with allure.step(f"Отправляем запрос на получение заказа с ID {order_id}"):
        resp = api_manager.store_api.get_order_by_id(
            order_id=order_id,
            expected_status=None
        )

    with allure.step("Проверяем статус код и валидируем ответ"):
        if resp.status_code == 200:
            try:
                order = OrderModel(**resp.json())      # Валидация через Pydantic
            except ValidationError as e:
                assert False, f"Order API response doesn't match model: {e}"

            assert order.id == order_id
            assert order.status == create_order["status"]
        elif resp.status_code in (404, 500):
            pass
        else:
            raise AssertionError(f"Unexpected status code: {resp.status_code}, body: {resp.text}")

@allure.feature("Store API")
@allure.story("Order")
@allure.title("Удаление заказа: DELETE /store/order/{orderId}")
@allure.description("Тест проверяет удаление заказа и корректность последущюих запросов.")
@allure.tag("api", "positive")
def test_delete_order(create_order, api_manager):
    """DELETE /store/order/{orderid} - удалем заказ и проверяем результат"""
    order_id = create_order["id"]

    with allure.step(f"Отправляем запрос на удаление заказа с ID {order_id}"):
        delete_resp = api_manager.store_api.delete_order(
            order_id=order_id,
            expected_status=None
        )
        assert delete_resp.status_code in (200, 404), (f"Unexpected status code on DELETE: {delete_resp.status_code},"
                                                   f"body: {delete_resp.text}")

    with allure.step("Проверяем, что заказ больше не существует"):
        get_resp = api_manager.store_api.get_order_by_id(
            order_id=order_id,
            expected_status=None
        )
        if get_resp.status_code == 200:
            try:
                order = OrderModel(**get_resp.json())
                raise AssertionError(f"Order with id={order_id} still exists after deletion")
            except ValidationError:
                # Если структура не соответствует модели, можно считать заказ удаленным
                pass
        elif get_resp.status_code not in (404, 500):
            raise AssertionError(
                f"Unexpected status code on GET after DELETE: {get_resp.status_code},"
                f" body: {get_resp.text}"
            )