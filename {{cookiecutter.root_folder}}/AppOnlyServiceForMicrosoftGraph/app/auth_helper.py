import base64
import json
import requests
import app.config as config

login_url = 'https://login.microsoftonline.com/'
authorize_endpoint = '{0}{1}{2}'.format(login_url,config.tenant_id,'/oauth2/token')

bodyvals = {'client_id': config.client_id,
            'client_secret': config.client_secret,
            'grant_type': 'client_credentials',
            'resource':config.resource_endpoint}
# Get an OAuth access token
def get_token():
    return requests.post(authorize_endpoint, data=bodyvals)