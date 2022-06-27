from espo_api_client import EspoAPI
from datetime import date
import base64
import pprint
import json

client = EspoAPI('http://10.0.0.111', '3a6e01aeee51af096936fe7c6eb4dd06')

# Get accounts
def get_tender(broj_postupka):
    params = {
        "select": "",
        "where": [
            {
                "type": "like",
                "attribute": "brojPostupka",
                "value": broj_postupka,
            },
        ],
    }

    return client.request('GET', 'Tenderi', params)

# get_tender('1208-7-2-19-3-5/22')
tender = get_tender('320-1-1-256-3-191/22')

print(type(tender['total']))