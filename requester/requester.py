import requests
import logging
import os

# Цвета для вызова в консоль(для читабельности)
RED = "\033[91m"
GREEN = "\033[92m"
RESET = "\033[0m"

class CustomRequester:
    """
    Кастомный реквестер для удобной работы с API:
    - стандартизирует отправку запросов
    - умеет логировать запросы и ответы в curl-формате
    - опционально проверяет статус коды
    """

    # Задаем базовые заголовки по умолчанию, которые каждый экземпляр может менять
    base_headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    def __init__(self, base_url: str, session):
        self.session = session
        self.base_url = base_url
        self.headers = self.base_headers.copy()

        # Создаем логгер, который будет хранить имя файла и выставляем уровень с INFO
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    # Создаем основной метод, через который отправляем HTTP-запросы в тестах.
    # Собирает единый запрос: собирает url, посдтавляет метод.
    # Логирует запрос и проверяет статус-коды, возвращает response, чтобы в тесте сделать resp.json()
    def send_request(
        self,
        method: str,
        endpoint: str,
        data: dict = None,
        params: dict = None,
        expected_status: int | None = None,
        need_logging: bool = True,
    ) -> requests.Response:
        """Отправка запроса"""

        # Собираем полный url
        url = f"{self.base_url}{endpoint}"

        # Отправляем запрос, передав необходимые параметры:
        response = self.session.request(
            method=method,
            url=url,
            json=data,
            params=params,
            headers=self.headers
        )

        # Если need_logging True вызвать
        if need_logging:
            self.request_and_response(response)

        # Проверяем статус-код, если он передан в expected_status
        if expected_status is not None and response.status_code != expected_status:
            raise AssertionError(
                f"Unexpected status code: {response.status_code}. Expected: {expected_status}"
            )

        return response


    def request_and_response(self, response: requests.Response):
        """
        Логирует запрос и овтет в curl-формате.
        Метод делает удобный вывод в лог, похожий на curl, чтобы можно было:
        - скопировать команду и воспроизвести запрос в ручную
        - видеть заголовки и тело запроса
        - быстро прочитать тело ответа в случае ошибки
        """

        # Обернуть все в try / except, чтобы тест не падал в случае ошибки в логировании
        try:
            # Получаем исходный запрос
            request = response.request

            # Сформировать строку с заголовками в виде curl
            headers = " \\\n".join(
                [f"-H '{k}: {v}'" for k, v in request.headers.items()]
            )

            # Определяем имя текущего теста из pytest
            test_name = f"pytest {os.environ.get('PYTEST_CURRENT_TEST', '').replace('(call)', '')}"

            # Тело запроса
            body = ''
            if request.body:
                try:
                    body = request.body.decode() if isinstance(request.body, bytes) else request.body
                except Exception:
                    body = str(request.body)
                body = f"-d '{body}' \n"

                # Лог запроса
                self.logger.info(
                    f"{GREEN}{test_name}{RESET}\n"
                    f"curl -X {request.method} '{request.url}' \\\n"
                    f"{headers} \\\n"
                    f"{body}"
                )

                # Лог ответа. Логируем только если respons.ok == False
                if not response.ok:
                    self.logger.info(
                        f"\tRESPONSE:\nSTATUS: {RED}{response.status_code}{RESET}"
                        f"DATA: {RED}{response.text}{RESET}"
                    )

        except Exception as e:
            self.logger.info(f"Logging failed: {type(e)} - {e}")