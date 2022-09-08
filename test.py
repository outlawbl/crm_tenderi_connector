from configparser import ConfigParser
from espo_api_client import EspoAPI
import pprint

data_file = 'config.ini'
config = ConfigParser()
config.read(data_file)

espo_api_host = config['espo_api']['espo_api_host']
espo_api_key = config['espo_api']['espo_api_key']

client = EspoAPI(espo_api_host, espo_api_key)

att_id = '630e068a3f36cc5c9'
def delete_document(att_id):
    params = {
        "select": "id",
        "where": [
            {
                "type": "equals",
                "attribute": "fileId",
                "value": att_id,
            },
        ],
        }

    print(client.request('DELETE', 'Document', params))

def get_document(att_id):
    params = {
        "select": "id",
        "where": [
            {
                "type": "equals",
                "attribute": "fileId",
                "value": att_id,
            },
        ],
        }

    print(client.request('GET', 'Document', params))



# get_document(att_id)
['6308d0471057fc081', '6308cff023356840a']
# pprint.pprint(client.request('PUT', 'Tenderi/6308cfecea65e4b71', {'documentsIds': ['6308d0471057fc081', '6308cff023356840a', '630e068c44f395586']}))
# pprint.pprint(client.request('GET', 'Tenderi/6308cfecea65e4b71'))

# def get_tender_documents(entity, id):
#     response = client.request('GET', f'{entity}/{id}')
#     return response['documentsIds']

# print(get_tender_documents('Tenderi', '6308cfecea65e4b71'))

def get_document(attribute, value):
    params = {
        "select": "id",
        "where": [
            {
                "type": "equals",
                "attribute": attribute,
                "value": value,
            },
        ],
        }
    response = client.request('GET', 'Document', params)
    pprint.pprint(response)
    return response['list'][0]['id']

print(get_document('fileId', '6319ab669228813d0'))
