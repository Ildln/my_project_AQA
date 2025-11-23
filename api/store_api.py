import requests

from requester.requester import CustomRequester
from utils.endpoints import GET_STORE_INVENTORY_ENDPOINT, CREATE_STORE_ORDER_ENDPOINT, GET_STORE_ORDER_ID_ENDPOINT


class StoreApi(CustomRequester):
    """
    Создаем класс для работы с зказами из магазина Store.
    """

    def __init__(self, base_url: str, session: requests.Session):
        super().__init__(base_url=base_url, session=session)

    def get_inventory(self, expected_status=None):
        """
        Получаем информацию инвентаря. "GET /store/inventory"
        """
        return self.send_request(
            method="GET",
            endpoint=GET_STORE_INVENTORY_ENDPOINT,
            expected_status=expected_status
        )

    def create_store_order(self, order_data, expected_status=None):
        """
        Создание заказа. "POST /store/order/"
        """
        return self.send_request(
            method="POST",
            endpoint=CREATE_STORE_ORDER_ENDPOINT,
            data=order_data,
            expected_status=expected_status,
        )

    def get_order_by_id(self, order_id, expected_status=None):
        """
        Получение данных о заказе по id. "GET /store/order/{order_id}
        """
        return self.send_request(
            method="GET",
            endpoint=GET_STORE_ORDER_ID_ENDPOINT.format(order_id=order_id),
            expected_status=expected_status
        )

    def delete_order(self, order_id, expected_status=None):
        """
        Удаляем заказ по id. "DELETE /store/order/{order_id}
        """
        return self.send_request(
            method="DELETE",
            endpoint=GET_STORE_ORDER_ID_ENDPOINT.format(order_id=order_id),
            expected_status=expected_status
        )