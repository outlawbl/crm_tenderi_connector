from espo_api_client import EspoAPI
from datetime import date
import base64
import pprint
from datetime import date, datetime
import json
import logging
import re
import os

logging.basicConfig(filename='example.log', format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)

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

def get_account(pdf_data):
    # provjeri postoji li Pravno lice u CRM
    logging.info('Checking if account already exists...')
    jib = pdf_data['uo']['jib']
    params = {
        "select": "name",
        "where": [
            {
                "type": "equals",
                "attribute": "sicCode",
                "value": f'{jib}'
            },
        ],
    }
    response = client.request('GET', 'Account', params)
    pprint.pprint(response)
    return response


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

def post_account(acc_info):
    logging.info('Adding new account...')
    data = {
        'name': acc_info['name'],
        'sicCode': acc_info['jib']
    }
    response = client.request('POST', 'Account', data)
    posted_account_id = response['id']
    posted_account_name = response['name']
    logging.info(f'New account has been added: {posted_account_name}')
    return posted_account_id

def post_tender(pdf_data, account_id):
    logging.info('Adding new tender...')
    data = pdf_data['osnovni_podaci']
    data['accounts1Id'] = account_id
    data['tipTendera'] = "Objavljeni"
    data['createdAt'] = json.dumps(datetime.now(), indent=4, default=str)
    response = client.request('POST', 'Tenderi', data)
    tender_id = response['id']
    logging.info('New tender has been successfully added!')
    return tender_id

def post_document(file_path, tender_id):
# post attachment
    logging.info('Adding new document...')
    logging.info('    - Adding new attachment...')
    with open(file_path, "rb") as pdf_file:
        encoded_file = base64.b64encode(pdf_file.read()).decode()
        # regex_query = re.compile('(?<=watch_folder\/).*')
        # file_name = regex_query.findall(file_path)[0]
        file_name = os.path.basename(file_path)
    data = {
    "name": f"{file_name}",
    "type": "application/pdf",
    "role": "Attachment",
    "relatedType": "Document",
    "field": "file",
    "file": f"data:application/pdf;base64, {encoded_file}"
    }
    doc_id = (client.request('POST', 'Attachment', data))['id']

    today = date.today()
    publish_date = today.strftime("%Y-%m-%d")

    logging.info('    - Adding new document...')
    data = {
        "name": "Obavjestenje o nabavci",
        "fileId": doc_id,
        "publishDate": publish_date,
        "status": "Active",
        "tenderisIds": [f"{tender_id}"],
        "folderId": "62552a7b40dcbca04",
        "assignedUserId": "1"
        }
    client.request('POST', 'Document', data)
    logging.info('New document has been successfully added!')
# post_document()