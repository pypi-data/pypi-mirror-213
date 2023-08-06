from pandas import DataFrame
from zeep.helpers import serialize_object
from zeep import Settings
from zeep import Client

class nmbrsapi:
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
						_soapheaders=header_value
					)
				)
		if request_data is not None:
			result = serialize_object(
					getattr(client.service, call)(
						**request_data,
						_soapheaders=header_value
					)
				)

		return result

