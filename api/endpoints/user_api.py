import requests

from requester.requester import CustomRequester
from utils.endpoints import CREATE_USER_ENDPOINT, GET_USER_BY_NAME_ENDPOINT, LOGIN_USER_ENDPOINT, LOGOUT_USER_ENDPOINT


class UserApi(CustomRequester):
    """
    Класс для работы с пользователями.
    """

    def __init__(self, base_url: str, session: requests.Session):
        super().__init__(session=session, base_url=base_url)

    def create_user(self, user_data, expected_status=None):
        """
        Создание нового пользователя
        """
        return self.send_request(
            method="POST",
            endpoint=CREATE_USER_ENDPOINT,
            data=user_data,
            expected_status=expected_status,
        )

    def get_user_by_name(self, username, expected_status):
        """
        Получения пользователя по username
        """
        endpoint = GET_USER_BY_NAME_ENDPOINT.format(username=username)
        return self.send_request(
            method="GET",
            endpoint=endpoint,
            expected_status=expected_status
        )

    def login(self, username: str, password: str, expected_status=None):
        """
        Логин пользователя с переданными username, password
        """
        return self.send_request(
            method="GET",
            endpoint=LOGIN_USER_ENDPOINT,
            params={"username": username, "password": password},
            expected_status=expected_status
        )

    def logout(self, expected_status=None):
        """
        Выход пользователя
        """
        return self.send_request(
            method="GET",
            endpoint=LOGOUT_USER_ENDPOINT,
            expected_status=expected_status
        )