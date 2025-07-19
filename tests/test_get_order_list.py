import pytest
import allure
import requests
from data import Url
from data import DataForOrder  # Предположим, здесь order_data с валидными данными


@pytest.fixture(scope='function')
def create_test_order():
    with allure.step("Создание тестового заказа через API"):
        response = requests.post(
            url=f"{Url.MAIN_URL}{Url.CREATE_ORDER}",
            json=DataForOrder.order_data
        )
        assert response.status_code == 201, f"Не удалось создать заказ, статус: {response.status_code}, тело: {response.text}"

    yield  # ничего не возвращаем — заказ сохраняется на сервере, ID не нужен

    # Удаление не требуется, так как нет API для удаления заказа (предположительно)


@allure.epic('Order API')
class TestOrderList:

    @allure.title('Проверка получения списка заказов')
    def test_get_orders_list(self, create_test_order):
        with allure.step("Отправка GET-запроса на получение списка заказов"):
            response = requests.get(f"{Url.MAIN_URL}{Url.GET_ORDER_LIST}")
            assert response.status_code == 200, f"Ожидался статус 200, но получили {response.status_code}"

        with allure.step("Проверка структуры ответа и ключей заказа"):
            data = response.json()
            orders = data.get("orders") or data.get("data")

            assert orders is not None, "В ответе отсутствует список заказов (ключ 'orders' или 'data')"
            assert isinstance(orders, list), f"Ожидается список заказов, получили {type(orders)}"
            assert len(orders) > 0, "Список заказов пуст, хотя должен содержать хотя бы один заказ"

            sample_order = orders[0]
            assert isinstance(sample_order, dict), "Ожидается, что заказ — это объект (dict)"

            expected_keys = {"id", "address", "color", "comment", "firstName", "lastName", "phone", "deliveryDate"}
            for key in expected_keys:
                assert key in sample_order, f"В заказе отсутствует ключ '{key}'"
