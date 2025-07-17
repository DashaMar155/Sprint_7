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

    response_create = requests.post(
        url=f"{Url.MAIN_URL}{Url.CREATE_COURIER}",
        json=create_body
    )
    assert response_create.status_code == 201, f"Создание курьера не удалось: {response_create.text}"

    yield create_body, login_body

    # После теста удаляем курьера
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
        response = requests.post(
            url=f'{Url.MAIN_URL}{Url.COURIER_LOGIN}',
            json=create_courier[1]
        )
        assert response.status_code == 200
        assert response.json().get("id") is not None

    @allure.title('Login with unregistered courier')
    def test_unregistered_courier_login(self):
        login_data = {
            'login': f"user_{uuid.uuid4().hex[:8]}",
            'password': "randomPass123"
        }
        response = requests.post(
            url=f'{Url.MAIN_URL}{Url.COURIER_LOGIN}',
            json=login_data
        )
        assert response.status_code == 404
        assert response.json() == ResponseBody.COURIER_ACCOUNT_NOT_FOUND

    @allure.title('Login with empty password')
    def test_courier_login_empty_password_error(self, create_courier):
        data = {
            'login': create_courier[0]['login'],
            'password': ''
        }
        response = requests.post(
            url=f'{Url.MAIN_URL}{Url.COURIER_LOGIN}',
            json=data
        )
        assert response.status_code == 400
        assert response.json() == ResponseBody.COURIER_LOGIN_NOT_ENOUGH_DATA

    @allure.title('Login with empty login')
    def test_courier_login_empty_login_error(self, create_courier):
        data = {
            'login': '',
            'password': create_courier[0]['password']
        }
        response = requests.post(
            url=f'{Url.MAIN_URL}{Url.COURIER_LOGIN}',
            json=data
        )
        assert response.status_code == 400
        assert response.json() == ResponseBody.COURIER_LOGIN_NOT_ENOUGH_DATA
