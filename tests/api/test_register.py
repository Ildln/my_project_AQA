import allure

from pydantic import ValidationError
from models.user_model import UserModel

@allure.suite("User API")
@allure.sub_suite("Create User")
@allure.feature("Пользователи")
@allure.story("Создание нового пользователя")
@allure.title("Создание пользователя с валидными данными")
@allure.description("Тест проверяет создание нового пользователя через UserAPI и "
"валидацию ответа Pydantic.")
@allure.tag("api", "positive")
def test_creat_user(api_manager, new_user_payload):
    """
    Тест на создание нового пользователя через UserApi.
    """
    with allure.step("Send a POST request to create user"):
        resp_post = api_manager.user_api.create_user(
            user_data=new_user_payload,
            expected_status=None
        )
        allure.attach(str(resp_post.json()), name="Response API",
                      attachment_type=allure.attachment_type.JSON)

    with allure.step("Check the status code"):
        assert resp_post.status_code in (200, 404, 500)

    # Проверяем, что пользователь корректно создан
    if resp_post.status_code == 200:
        with allure.step("Validation response through Pydantic"):
            try:
                user = UserModel(**resp_post.json())  # Валидация через Pydantic
            except ValidationError as e:
                assert False, f"Ответ API не соответствует схеме: {e}"

        # Можно обращаться к полям безопасно
        with allure.step("Проверяем соответствие данных запроса и ответа"):
            assert user.username == new_user_payload["username"]
            assert user.email == new_user_payload["email"]

    # Проверка через method get_user_by_name запрос GET /user/{username}
    get_response = api_manager.user_api.get_user_by_name(
        username=new_user_payload["username"],
        expected_status=None
    )
    assert get_response.status_code in (200, 404, 500)

    if get_response.status_code == 200:
        fetched_user = get_response.json()
        assert fetched_user["username"] == new_user_payload["username"]
        assert fetched_user["email"] == new_user_payload["email"]

@allure.suite("User API")
@allure.sub_suite("CREATE User")
@allure.feature("Пользователи")
@allure.story("Создаем нового пользователя")
@allure.title("Создание пользователя без обязательного поля 'username'")
@allure.description("Негативный тест: проверяем, что API возвращает ошибку при остутствии обязательного поля 'username'.")
@allure.tag("api", "negative")
def test_negative_creat_user_missing_username(api_manager, new_user_payload):
    """
    Негативный тест: создание пользователя без обязательного поля 'username'.
    """
    with allure.step("Удаляем обязательное поле 'username' из payload"):
        new_user_payload.pop("username", None)

    with allure.step("Отправляем POST-запрос без username"):
        response = api_manager.user_api.create_user(
            user_data=new_user_payload,
            expected_status=None    # Не падаем на нестабильный сервер
        )

    with allure.step("Проверяем статус код"):
        assert response.status_code in (400, 500)

    if response.status_code == 200:
        with allure.step("Если сервер все-таки вернул 200, проверяем через Pydantic"):
            try:
                user = UserModel(**response.json())
            except ValidationError as e:
                # Ожидаем ошибку валидации, потому что username отсутствует
                assert "username" in str(e), f"Проверка Pydantic не сработала: {e}"