import pytest
import allure
import requests
from data import Url


@allure.epic('Order API')
class TestOrderList:

    @allure.title('Проверка получения списка заказов')
    def test_get_orders_list(self):
        response = requests.get(f"{Url.MAIN_URL}{Url.GET_ORDER_LIST}")

        assert response.status_code == 200, f"Ожидался статус 200, но получили {response.status_code}"

        data = response.json()
        orders = data.get("orders") or data.get("data")
        assert orders is not None, "В ответе отсутствует список заказов (ключ 'orders' или 'data')"
        assert isinstance(orders, list), f"Ожидается список заказов, получили {type(orders)}"

        if orders:
            sample_order = orders[0]
            assert isinstance(sample_order, dict), "Заказ должен быть объектом"

            # Используем реальные поля из ответа API
            expected_keys = {"id", "address", "color", "comment", "firstName", "lastName", "phone", "deliveryDate"}
            for key in expected_keys:
                assert key in sample_order, f"В заказе отсутствует ключ '{key}'"
