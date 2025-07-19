import pytest
import requests
import uuid
import allure
import generators
from data import Url, ResponseBody


@pytest.fixture(scope="function")
def create_courier():
    login = generators.login_generator() + "_" + uuid.uuid4().hex[:6]
    password = generators.password_generator()
    firstName = generators.name_generator()

    create_body = {
        'login': login,
        'password': password,
        'firstName': firstName
    }

    login_body = {
        'login': login,
        'password': password
    }

    # Создание курьера
    with allure.step("Создание курьера через API"):
        response_create = requests.post(
            url=f"{Url.MAIN_URL}{Url.CREATE_COURIER}",
            json=create_body
        )
        # Проверка будет в тесте

    # Логин курьера
    with allure.step("Авторизация созданного курьера для получения ID"):
        response_login = requests.post(
            url=f"{Url.MAIN_URL}{Url.COURIER_LOGIN}",
            json=login_body
        )
        courier_id = response_login.json().get('id')

    yield create_body, login_body, courier_id

    # Удаление после теста
    with allure.step("Удаление курьера после теста"):
        delete_resp = requests.delete(
            url=f"{Url.MAIN_URL}{Url.COURIER_DELETE}{courier_id}"
        )
        assert delete_resp.status_code in [200, 204], f"Удаление курьера не удалось: {delete_resp.text}"


class TestsCreateNewCourier:

    @allure.title("Успешное создание нового курьера")
    def test_creation_courier_success(self, create_courier):
        create_body, login_body, courier_id = create_courier

        with allure.step("Отправка запроса на создание курьера"):
            response = requests.post(
                url=f"{Url.MAIN_URL}{Url.CREATE_COURIER}",
                json=create_body
            )

        with allure.step("Проверка, что курьер создан"):
            assert response.status_code == 201, f"Ожидался статус 201, но пришёл {response.status_code}"
            assert response.json() == ResponseBody.COURIER_CREATED, "Ответ не совпадает с ожидаемым"

        with allure.step("Проверка авторизации курьера"):
            response_login = requests.post(
                url=f"{Url.MAIN_URL}{Url.COURIER_LOGIN}",
                json=login_body
            )
            assert response_login.status_code == 200, f"Ожидался статус 200 при логине, но пришёл {response_login.status_code}"
            assert response_login.json().get("id") == courier_id, "ID курьера не совпадает"

    @allure.title("Ошибка при попытке создать дубликат курьера")
    def test_creation_courier_clone_error(self, create_courier):
        create_body, _, _ = create_courier

        with allure.step("Попытка создать курьера с тем же логином"):
            response = requests.post(
                url=f"{Url.MAIN_URL}{Url.CREATE_COURIER}",
                json=create_body
            )

        with allure.step("Проверка, что вернулся 409 и сообщение об ошибке"):
            assert response.status_code == 409, f"Ожидался 409, получен {response.status_code}"
            assert response.json() == ResponseBody.COURIER_NAME_ALREADY_EXIST
