import pytest
import requests
import allure
import uuid
from data import Url, ResponseBody


@pytest.fixture(scope="function")
def create_courier():
    unique_login = f"user_{uuid.uuid4().hex[:8]}"
    password = "password123"
    firstName = "TestName"

    create_body = {
        'login': unique_login,
        'password': password,
        'firstName': firstName
    }
    login_body = {
        'login': unique_login,
        'password': password
    }

    with allure.step("Создание курьера через API"):
        response_create = requests.post(
            url=f"{Url.MAIN_URL}{Url.CREATE_COURIER}",
            json=create_body
        )
    assert response_create.status_code == 201, f"Создание курьера не удалось: {response_create.text}"

    yield create_body, login_body

    with allure.step("Удаление курьера после теста"):
        response_login = requests.post(
            url=f"{Url.MAIN_URL}{Url.COURIER_LOGIN}",
            json=login_body
        )
        if response_login.status_code == 200:
            courier_id = response_login.json().get('id')
            if courier_id:
                requests.delete(f"{Url.MAIN_URL}{Url.COURIER_DELETE}{courier_id}")


@allure.epic('Courier API')
class TestLoginCourier:

    @allure.title('Successful courier login')
    def test_successful_courier_login(self, create_courier):
        with allure.step("Логин созданного курьера"):
            response = requests.post(
                url=f'{Url.MAIN_URL}{Url.COURIER_LOGIN}',
                json=create_courier[1]
            )

        with allure.step("Проверка успешного логина"):
            assert response.status_code == 200
            assert response.json().get("id") is not None

    @pytest.mark.parametrize(
        "login_data, expected_status, expected_response, title",
        [
            (
                {
                    'login': f"user_{uuid.uuid4().hex[:8]}",
                    'password': "randomPass123"
                },
                404,
                ResponseBody.COURIER_ACCOUNT_NOT_FOUND,
                "Login with unregistered courier"
            ),
            (
                {
                    'login': "some_existing_login",  # Для примера, если нужно можно менять
                    'password': ""
                },
                400,
                ResponseBody.COURIER_LOGIN_NOT_ENOUGH_DATA,
                "Login with empty password"
            ),
            (
                {
                    'login': "",
                    'password': "somepassword"
                },
                400,
                ResponseBody.COURIER_LOGIN_NOT_ENOUGH_DATA,
                "Login with empty login"
            )
        ]
    )
    def test_invalid_logins(self, login_data, expected_status, expected_response, title, create_courier):
        # В случае тестов с пустым логином/паролем используем create_courier фикстуру для получения валидных данных
        if login_data['login'] == "some_existing_login":
            login_data['login'] = create_courier[0]['login']
        if login_data['password'] == "somepassword":
            login_data['password'] = create_courier[0]['password']

        with allure.step(f"{title} - отправка POST запроса на логин"):
            response = requests.post(
                url=f'{Url.MAIN_URL}{Url.COURIER_LOGIN}',
                json=login_data
            )

        with allure.step(f"{title} - проверка ответа"):
            assert response.status_code == expected_status
            assert response.json() == expected_response
