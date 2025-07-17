import pytest
import requests
import generators
from data import Url

@pytest.fixture(scope="function")
def create_courier():
    login = generators.login_generator()
    password = generators.password_generator()
    name = generators.name_generator()

    create_courier_body = {
        'login': login,
        'password': password,
        'firstName': name
    }

    login_courier_body = {
        'login': login,
        'password': password
    }

    # Создаём курьера
    response_create = requests.post(
        url=f"{Url.MAIN_URL}{Url.CREATE_COURIER}",
        json=create_courier_body
    )
    assert response_create.status_code == 201 or response_create.status_code == 409

    # Логинимся, чтобы получить id
    response_login = requests.post(
        url=f"{Url.MAIN_URL}{Url.COURIER_LOGIN}",
        json=login_courier_body
    )
    assert response_login.status_code == 200

    courier_id = response_login.json().get('id')
    assert courier_id is not None

    yield create_courier_body, login_courier_body, courier_id

    # Удаляем курьера после теста
    requests.delete(
        url=f"{Url.MAIN_URL}{Url.COURIER_DELETE}{courier_id}"
    )
