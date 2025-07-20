import requests
import allure
import generators
import uuid
from data import Url, ResponseBody


@allure.epic("Courier API")
@allure.feature("Create courier")
class TestsCreateNewCourier:

    @allure.title("Успешное создание нового курьера")
    def test_creation_courier_success(self):
        login = generators.login_generator() + "_" + uuid.uuid4().hex[:6]
        password = generators.password_generator()
        name = generators.name_generator()

        create_body = {
            'login': login,
            'password': password,
            'firstName': name
        }

        login_body = {
            'login': login,
            'password': password
        }

        with allure.step("Создание курьера"):
            response = requests.post(
                url=f"{Url.MAIN_URL}{Url.CREATE_COURIER}",
                json=create_body
            )
            assert response.status_code == 201
            assert response.json() == ResponseBody.COURIER_CREATED

        with allure.step("Авторизация курьера для получения ID"):
            response_login = requests.post(
                url=f"{Url.MAIN_URL}{Url.COURIER_LOGIN}",
                json=login_body
            )
            assert response_login.status_code == 200
            courier_id = response_login.json().get("id")
            assert courier_id is not None

        with allure.step("Удаление курьера"):
            response_delete = requests.delete(
                url=f"{Url.MAIN_URL}{Url.COURIER_DELETE}{courier_id}"
            )
            assert response_delete.status_code in [200, 204]

    @allure.title("Ошибка при попытке создать курьера с уже существующим логином")
    def test_creation_courier_clone_error(self):
        login = generators.login_generator() + "_" + uuid.uuid4().hex[:6]
        password = generators.password_generator()
        name = generators.name_generator()

        create_body = {
            'login': login,
            'password': password,
            'firstName': name
        }

        with allure.step("Создание оригинального курьера"):
            response_create = requests.post(
                url=f"{Url.MAIN_URL}{Url.CREATE_COURIER}",
                json=create_body
            )
            assert response_create.status_code == 201

        with allure.step("Повторная попытка создать курьера с тем же логином"):
            response_duplicate = requests.post(
                url=f"{Url.MAIN_URL}{Url.CREATE_COURIER}",
                json=create_body
            )
            assert response_duplicate.status_code == 409
            assert response_duplicate.json() == ResponseBody.COURIER_NAME_ALREADY_EXIST

        with allure.step("Удаление оригинального курьера"):
            response_login = requests.post(
                url=f"{Url.MAIN_URL}{Url.COURIER_LOGIN}",
                json={'login': login, 'password': password}
            )
            courier_id = response_login.json().get("id")
            if courier_id:
                requests.delete(f"{Url.MAIN_URL}{Url.COURIER_DELETE}{courier_id}")
