import pytest
import requests
import generators
import uuid
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

    response_create = requests.post(
        url=f"{Url.MAIN_URL}{Url.CREATE_COURIER}",
        json=create_body
    )
    assert response_create.status_code == 201, f"Создание курьера не удалось: {response_create.text}"

    response_login = requests.post(
        url=f"{Url.MAIN_URL}{Url.COURIER_LOGIN}",
        json=login_body
    )
    assert response_login.status_code == 200, f"Логин курьера не удался: {response_login.text}"

    courier_id = response_login.json().get('id')
    assert courier_id is not None, "ID курьера не получен"

    yield create_body, login_body, courier_id

    delete_resp = requests.delete(
        url=f"{Url.MAIN_URL}{Url.COURIER_DELETE}{courier_id}"
    )
    assert delete_resp.status_code in [200, 204], f"Удаление курьера не удалось: {delete_resp.text}"


class TestsCreateNewCourier:

    def test_creation_courier_success(self, create_courier):
        pass  # фикстура сама делает все проверки

    def test_creation_courier_clone_error(self, create_courier):
        # Попытка создать курьера с тем же логином — ожидаем 409
        response = requests.post(
            url=f"{Url.MAIN_URL}{Url.CREATE_COURIER}",
            json=create_courier[0]
        )
        assert response.status_code == 409, f"Ожидался 409, получен {response.status_code}"
        assert response.json() == ResponseBody.COURIER_NAME_ALREADY_EXIST
