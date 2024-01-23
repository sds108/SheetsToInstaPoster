import requests
import json

def getCreds() :
	""" Get creds required for use in the applications
	
	Returns:
		dictonary: credentials needed globally
	"""
	with open('ig_data.json', encoding='utf-8') as j:
		info = json.loads(j.read())

	creds = dict() # dictionary to hold everything
	creds['access_token'] = ''#info['access_token']#'' # access token for use with all api calls
	creds['graph_domain'] = info['graph_domain']#'https://graph.facebook.com/' # base domain for api calls
	creds['graph_version'] = info['graph_version']#'v12.0' # version of the api we are hitting
	creds['endpoint_base'] = creds['graph_domain'] + creds['graph_version'] + '/' # base endpoint with domain and version
	creds['instagram_account_id'] = info['instagram_account_id']#'' # users instagram account id
	creds['client_id'] = info['client_id']#'' # client id from facebook app IG Graph API Test
	creds['client_secret'] = info['client_secret']#'' # client secret from facebook app
	creds['page_id'] = info['page_id']#'' # users page id

	return creds

def makeApiCall(url, endpointParams, type) :
	""" Request data from endpoint with params
	
	Args:
		url: string of the url endpoint to make request from
		endpointParams: dictionary keyed by the names of the url parameters
	Returns:
		object: data from the endpoint
	"""

	if type == 'POST' : # post request
		data = requests.post(url, endpointParams)
	else : # get request
		data = requests.get(url, endpointParams)

	response = dict() # hold response info
	response['url'] = url # url we are hitting
	response['endpoint_params'] = endpointParams #parameters for the endpoint
	response['endpoint_params_pretty'] = json.dumps(endpointParams, indent = 4) # pretty print for cli
	response['json_data'] = json.loads( data.content ) # response data from the api
	response['json_data_pretty'] = json.dumps(response['json_data'], indent = 4) # pretty print for cli

	return response # get and return content