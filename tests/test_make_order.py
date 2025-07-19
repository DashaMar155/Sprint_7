import pytest
import requests
import allure
from data import Url, DataForOrder, Flags


@allure.epic("Scooter Order API")
@allure.feature("Order Creation")
@allure.story("Create order with different scooter colors")
class TestCreationOrder:

    @pytest.mark.parametrize('color', DataForOrder.scooter_color)
    @allure.title("Create order with color: {color}")
    def test_create_order_with_color_variations(self, color):
        with allure.step("Prepare order data"):
            order_data = DataForOrder.order_data.copy()
            order_data['color'] = color
            allure.attach(str(order_data), name="Order Data", attachment_type=allure.attachment_type.JSON)

        with allure.step("Send POST request to create order"):
            response = requests.post(
                url=f"{Url.MAIN_URL}{Url.CREATE_ORDER}",
                json=order_data
            )
            allure.attach(response.text, name="Response Body", attachment_type=allure.attachment_type.JSON)

        with allure.step("Verify response status code is 201"):
            assert response.status_code == 201, \
                f"Expected status 201, got {response.status_code}. Response: {response.text}"

        with allure.step("Verify response contains track"):
            response_json = response.json()
            assert Flags.SUCCESSFUL_ORDER_CREATION in response_json, \
                f"Response JSON does not contain '{Flags.SUCCESSFUL_ORDER_CREATION}': {response_json}"

            track = response_json[Flags.SUCCESSFUL_ORDER_CREATION]
            assert track, "Track is empty or None"
            allure.attach(str(track), name="Track", attachment_type=allure.attachment_type.TEXT)
