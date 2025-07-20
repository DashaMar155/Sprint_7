import pytest
import requests
import generators
import logging
from data import Url

# Настройка логирования (если его ещё нет)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

    # Создание курьера
    response_create = requests.post(
        url=f"{Url.MAIN_URL}{Url.CREATE_COURIER}",
        json=create_courier_body
    )
    if response_create.status_code not in [201, 409]:
        pytest.fail(f"Не удалось создать курьера. Статус: {response_create.status_code}, Ответ: {response_create.text}")

    # Авторизация курьера
    response_login = requests.post(
        url=f"{Url.MAIN_URL}{Url.COURIER_LOGIN}",
        json=login_courier_body
    )
    if response_login.status_code != 200:
        pytest.fail(f"Не удалось залогиниться. Статус: {response_login.status_code}, Ответ: {response_login.text}")

    courier_id = response_login.json().get('id')
    if not courier_id:
        pytest.fail("ID курьера не получен при логине")

    yield create_courier_body, login_courier_body, courier_id

    # Удаление курьера после теста
    response_delete = requests.delete(
        url=f"{Url.MAIN_URL}{Url.COURIER_DELETE}{courier_id}"
    )
    if response_delete.status_code not in [200, 204]:
        logger.error(f"Не удалось удалить курьера после теста. Статус: {response_delete.status_code}, Ответ: {response_delete.text}")
