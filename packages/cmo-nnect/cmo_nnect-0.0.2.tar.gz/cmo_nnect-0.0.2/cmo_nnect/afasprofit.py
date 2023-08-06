import requests
import base64
from pandas import DataFrame

class AfasProfit:
	def __init__(
		self,
		profit_token: str,
		company_id: int,
		environment: str = ''
	):
		self.company_id = company_id
		self.base_url = f"https://{str(company_id)}.rest{environment}.afas.online/ProfitRestServices/connectors/"
		self.authorization = {"Authorization": "AfasToken " + base64.b64encode(profit_token.encode('ascii')).decode('ascii')}

	def connection_test(self) -> DataFrame:
		"""Function that calls the AFAS Profit API metainfo endpoint to test the connection."""

		profit_response = requests.get(
			f"https://{str(self.company_id)}.rest.afas.online/ProfitRestServices/metainfo",
			headers=self.authorization
		)

		if profit_response.status_code == 200:
			test_result = "Success!"
		else:
			test_result = "Connection failed. Please check the credentials."
		
		return test_result

	
	def get_data(self, connector_name: str, params: str = None) -> DataFrame:
		"""Function that sends a API call to the AFAS Profit API to extract data and return it into a DataFrame.
		"""
		# Send a get request to the AFAS API for the specific get connector
		profit_response = requests.get(
			f"https://{str(self.company_id)}.rest.afas.online/ProfitRestServices/connectors/{connector_name}",
			params=params,
			headers=self.authorization
		)

		profit_data = DataFrame(profit_response.json()["rows"])

		return profit_data


