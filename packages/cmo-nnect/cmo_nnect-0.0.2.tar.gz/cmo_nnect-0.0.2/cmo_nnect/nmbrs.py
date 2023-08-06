from pandas import DataFrame
from zeep.helpers import serialize_object
from zeep import Settings
from zeep import Client
from collections import OrderedDict

class Nmbrs:
	def __init__(
		self,
		username: str,
		token: int
	):
		self.header_value = {
				"AuthHeaderWithDomain" : {
				"Username" : username,
				"Token" : token
				}
		}

	def _flatten_ordered_dicts(self, ordered_dicts):
		flattened_rows = []

		def flatten_dict(ordered_dict, parent_key=''):
			for key, value in ordered_dict.items():
				new_key = f"{key}" if parent_key else key

				if isinstance(value, OrderedDict):
					flatten_dict(value, parent_key=new_key)
				elif isinstance(value, list) and all(isinstance(item, OrderedDict) for item in value):
					for item in value:
						flatten_dict(item, parent_key=new_key)
				else:
					flattened_row[new_key] = value

		for ordered_dict in ordered_dicts:
			flattened_row = {}
			flatten_dict(ordered_dict)
			flattened_rows.append(flattened_row)

		return flattened_rows

	def get_data(self, service: str, call: str, request_data: dict = None):
		"""Function to call the Zeep API through SOAP.
		
		This function intializes a connection object with a specific service.
		It then allows to make API calls either with or without extra arguments.
		It serializes the returned object to a list of nested dictionaries, to make the creation of a DataFrame easier."""
		
		# Define urls
		wsdl_url = 'https://api.nmbrs.nl/soap/v3/'+service+'.asmx?WSDL'
		settings = Settings(strict=False,
						xml_huge_tree=True)
						
		# Initialize zeep client
		client = Client(wsdl=wsdl_url, settings = settings)
		
		# Make call 
		if request_data is None:
			result = serialize_object(
					getattr(client.service, call)(
						_soapheaders=self.header_value
					)
				)
		if request_data is not None:
			result = serialize_object(
					getattr(client.service, call)(
						**request_data,
						_soapheaders=self.header_value
					)
				)

		# Transform to a dataframe
		result_df = DataFrame(self._flatten_ordered_dicts(result))

		return result_df

