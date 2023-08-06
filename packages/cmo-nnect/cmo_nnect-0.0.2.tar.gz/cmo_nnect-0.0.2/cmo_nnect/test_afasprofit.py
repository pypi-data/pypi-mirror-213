import unittest
from unittest.mock import patch, MagicMock
from pandas import DataFrame
from requests import Response

from .afasprofit import AfasProfit as afasprofit


class TestAfasProfit(unittest.TestCase):

    def setUp(self):
        self.profit_token = "your-profit-token"
        self.company_id = 12345
        self.environment = 'test'
        self.afas_profit = afasprofit(self.profit_token, self.company_id, self.environment)

    def test_connection_test_success(self):
        response_mock = MagicMock(spec=Response)
        response_mock.status_code = 200

        with patch('requests.get', return_value=response_mock):
            result = self.afas_profit.connection_test()

        self.assertEqual(result, "Success!")

    def test_connection_test_failure(self):
        response_mock = MagicMock(spec=Response)
        response_mock.status_code = 401

        with patch('requests.get', return_value=response_mock):
            result = self.afas_profit.connection_test()

        self.assertEqual(result, "Connection failed. Please check the credentials.")

    def test_get_data(self):
        connector_name = "your-connector-name"
        params = "your-params"

        response_mock = MagicMock(spec=Response)
        response_mock.status_code = 200
        response_mock.json.return_value = {"rows": []}

        with patch('requests.get', return_value=response_mock):
            result = self.afas_profit.get_data(connector_name, params)

        self.assertIsInstance(result, DataFrame)


if __name__ == '__main__':
    unittest.main()
