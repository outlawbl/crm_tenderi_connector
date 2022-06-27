from espo_api_client import EspoAPI
from datetime import date
import base64
import pprint

client = EspoAPI('http://10.0.0.77', '3a6e01aeee51af096936fe7c6eb4dd06')

# Get accounts
def get_accounts():
    params = {
        "select": "",
        "where": [
            {
                "type": "like",
                "attribute": "id",
                "value": '%%',
            },
        ],
    }

    client.request('GET', 'Tenderi', params)

def get_tender(broj_postupka):
    params = {
        "select": "",
        "where": [
            {
                "type": "like",
                "attribute": "brojPostupka",
                "value": broj_postupka
            },
            {
                "type": "equals",
                "attribute": "deleted",
                "value": 0
            }
        ],
    }

    return client.request('GET', 'Tenderi', params)


def post_document(file_name):
    # post attachment

    with open(file_name, "rb") as pdf_file:
        encoded_file = base64.b64encode(pdf_file.read()).decode()
        # new_encoded_file = encoded_file.decode()

    data = {
    "name": "test.pdf",
    "type": "application/pdf",
    "role": "Attachment",
    "relatedType": "Document",
    "field": "file",
    "file": f"data:application/pdf;base64, {encoded_file}"
    }
    doc_id = (client.request('POST', 'Attachment', data))['id']

    today = date.today()
    publish_date = today.strftime("%Y-%m-%d")

    data = {
        "name": "test",
        "fileId": doc_id,
        "publishDate": publish_date,
        "status": "Active"
        }
    pprint.pprint(client.request('POST', 'Document', data))

# post_document()