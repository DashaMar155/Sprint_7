import pytest
import requests
import allure
import uuid
from data import Url, ResponseBody


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

    @allure.title('Login with unregistered courier')
    def test_login_unregistered_courier(self):
        login_data = {
            'login': f"user_{uuid.uuid4().hex[:8]}",
            'password': "randomPass123"
        }
        with allure.step("Отправка POST запроса на логин с несуществующим пользователем"):
            response = requests.post(
                url=f'{Url.MAIN_URL}{Url.COURIER_LOGIN}',
                json=login_data
            )
        with allure.step("Проверка ответа 404 и текста ошибки"):
            assert response.status_code == 404
            assert response.json() == ResponseBody.COURIER_ACCOUNT_NOT_FOUND

    @allure.title('Login with empty password')
    def test_login_empty_password(self, create_courier):
        login_data = {
            'login': create_courier[0]['login'],
            'password': ""
        }
        with allure.step("Отправка POST запроса на логин с пустым паролем"):
            response = requests.post(
                url=f'{Url.MAIN_URL}{Url.COURIER_LOGIN}',
                json=login_data
            )
        with allure.step("Проверка ответа 400 и текста ошибки"):
            assert response.status_code == 400
            assert response.json() == ResponseBody.COURIER_LOGIN_NOT_ENOUGH_DATA

    @allure.title('Login with empty login')
    def test_login_empty_login(self, create_courier):
        login_data = {
            'login': "",
            'password': create_courier[0]['password']
        }
        with allure.step("Отправка POST запроса на логин с пустым логином"):
            response = requests.post(
                url=f'{Url.MAIN_URL}{Url.COURIER_LOGIN}',
                json=login_data
            )
        with allure.step("Проверка ответа 400 и текста ошибки"):
            assert response.status_code == 400
            assert response.json() == ResponseBody.COURIER_LOGIN_NOT_ENOUGH_DATA
