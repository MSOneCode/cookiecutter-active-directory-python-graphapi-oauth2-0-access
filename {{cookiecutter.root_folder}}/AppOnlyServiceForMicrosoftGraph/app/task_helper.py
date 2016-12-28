import json
from requests import request

base_endpoint = 'https://graph.microsoft.com/'
version = 'v1.0/'

def invoke(access_token, api, method='GET', params={}, data=None):
    headers = {'Authorization':'Bearer'+' '+access_token,'Content-Type':'application/json'}
    url = '{}{}{}'.format(base_endpoint,version,api)
    req = request(method,url,headers=headers, data=json.dumps(data) ,params=params)
    return req