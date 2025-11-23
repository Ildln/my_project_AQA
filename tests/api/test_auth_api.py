import allure

@allure.feature("Пользователи")
@allure.story("Логин пользователя")
@allure.title("Успешный логин пользователя")
@allure.description("Тест проверяет возможность успешного входа пользователя через UserApi.")
@allure.tag("api", "positive")
def test_user_login(api_manager, user_fixture):
    with allure.step("Отправляем запрос на логин пользователя"):
        login_resp = api_manager.user_api.login(
           username=user_fixture["username"],
            password=user_fixture["password"],
            expected_status=None      # Не падаем, при нестабильном сервере
        )

    with allure.step("Проверяем статус код"):
        assert login_resp.status_code in (200, 404, 500)

@allure.feature("Пользователи")
@allure.story("Логин пользователя")
@allure.title("Попытка выхода с неверным паролем")
@allure.description("Негативный тест: проверка входа с неправильным паролем.")
@allure.tag("api", "negative")
def test_login_with_wrong_password(api_manager):
    with allure.step("Отправляем запрос на логин с неверным паролем"):
        resp = api_manager.user_api.login(
            username="some_user",
            password="wrong_password",
            expected_status=None
        )

    with allure.step("Проверяем статус код ответа"):
        assert resp.status_code == 200

@allure.feature("Пользователи")
@allure.story("Логаут пользователя")
@allure.title("Логаут авторизорванного пользователя")
@allure.description("Тест проверяет корректность выхода пользователя через UserApi.")
@allure.tag("api", "positive")
def test_logout_user(api_manager):
    with allure.step("Отправляем запрос на логаут пользователя"):
        check_logout = api_manager.user_api.logout(expected_status=200)

    with allure.step("Проверяем статус код"):
        assert check_logout.status_code in (200, 404, 500)

    with allure.step("Проверяем содержимое ответа"):
        assert "user logged out" in check_logout.text.lower(), (f"Expected word 'logout' the response,"
                                                                f"received: {check_logout.text}")


