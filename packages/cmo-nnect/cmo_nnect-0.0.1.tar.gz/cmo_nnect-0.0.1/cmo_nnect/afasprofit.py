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
		self.base_url = "https://" + str(company_id) + ".rest" + environment + ".afas.online/ProfitRestServices/connectors/"
		self.authorization = {"Authorization": "AfasToken " + base64.b64encode(profit_token.encode('ascii')).decode('ascii')}

	def get_data(self, connector_name: str, params: str) -> DataFrame:
		"""Function that calls the AFAS Profit API into a Spark Dataframe and outputs it to a Delta table.
		"""
		# Read folder in Synapse Link storage, using the model.json to extract metadata (headers)
		profit_response = requests.get(
			"https://" + str(self.company_id) + ".rest.afas.online/ProfitRestServices/connectors/" + connector_name,
			params=params,
			headers=self.authorization
		)

		return profit_response

