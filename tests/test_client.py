import unittest
from datetime import date, datetime
from unittest.mock import Mock, patch

from elprisenligenu.client import Client
from elprisenligenu.models import ElectricityPrice


class ClientTests(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    @patch("elprisenligenu.client.requests.get")
    def test_get_wraps_single_response_object(self, mock_get):
        api_response = {
            "DKK_per_kWh": 2.5,
            "EUR_per_kWh": 0.34,
            "EXR": 7.45,
            "time_start": "2024-01-01T00:00:00+00:00",
            "time_end": "2024-01-01T01:00:00+00:00",
        }
        mock_response = Mock(ok=True)
        mock_response.json.return_value = api_response
        mock_get.return_value = mock_response

        params = {"year": "2024", "month": "01", "day": "01", "area": "DK1"}
        prices = self.client._get(endpoint="prices", params=params)

        expected_url = (
            f"{self.client.base_url}/{self.client.version}/prices/2024/01-01_DK1.json"
        )
        mock_get.assert_called_once_with(expected_url, headers=self.client.HEADERS)
        self.assertEqual(len(prices), 1)

        price = prices[0]
        self.assertIsInstance(price, ElectricityPrice)
        self.assertEqual(price.dkk_per_kwh, api_response["DKK_per_kWh"])
        self.assertEqual(price.eur_per_kwh, api_response["EUR_per_kWh"])
        self.assertEqual(price.exchange_rate, api_response["EXR"])
        self.assertEqual(
            price.start, datetime.fromisoformat(api_response["time_start"])
        )
        self.assertEqual(price.end, datetime.fromisoformat(api_response["time_end"]))

    @patch("elprisenligenu.client.requests.get")
    def test_get_parses_list_response(self, mock_get):
        api_response = [
            {
                "DKK_per_kWh": 1.5,
                "EUR_per_kWh": 0.2,
                "EXR": 7.45,
                "time_start": "2024-02-03T00:00:00+00:00",
                "time_end": "2024-02-03T01:00:00+00:00",
            },
            {
                "DKK_per_kWh": 1.8,
                "EUR_per_kWh": 0.24,
                "EXR": 7.45,
                "time_start": "2024-02-03T01:00:00+00:00",
                "time_end": "2024-02-03T02:00:00+00:00",
            },
        ]
        mock_response = Mock(ok=True)
        mock_response.json.return_value = api_response
        mock_get.return_value = mock_response

        params = {"year": "2024", "month": "02", "day": "03", "area": "DK2"}
        prices = self.client._get(endpoint="prices", params=params)

        self.assertEqual(len(prices), 2)
        self.assertEqual(prices[0].dkk_per_kwh, 1.5)
        self.assertEqual(prices[1].eur_per_kwh, 0.24)
        self.assertEqual(
            prices[0].start, datetime.fromisoformat("2024-02-03T00:00:00+00:00")
        )
        self.assertEqual(
            prices[1].end, datetime.fromisoformat("2024-02-03T02:00:00+00:00")
        )

    def test_get_prices_iterates_over_date_range(self):
        day_one_prices = [ElectricityPrice(1.0, 0.1, 7.45, "", "")]
        day_two_prices = [ElectricityPrice(1.5, 0.2, 7.45, "", "")]

        with patch.object(
            Client, "_get", side_effect=[day_one_prices, day_two_prices]
        ) as mock_get:
            prices = list(
                self.client.get_prices(
                    start=date(2024, 5, 1), end=date(2024, 5, 2), area="DK2"
                )
            )

        self.assertEqual(prices, day_one_prices + day_two_prices)
        self.assertEqual(mock_get.call_count, 2)

        first_call = mock_get.call_args_list[0]
        second_call = mock_get.call_args_list[1]
        self.assertEqual(first_call.kwargs["endpoint"], "prices")
        self.assertEqual(second_call.kwargs["endpoint"], "prices")
        self.assertEqual(
            first_call.kwargs["params"],
            {"area": "DK2", "year": "2024", "month": "05", "day": "01"},
        )
        self.assertEqual(
            second_call.kwargs["params"],
            {"area": "DK2", "year": "2024", "month": "05", "day": "02"},
        )


if __name__ == "__main__":
    unittest.main()
