import imp
from api import client
from datetime import date, datetime
import base64
import pprint
import re
import json

def main_function(pdf_data, file_path):
    
    def post_account(acc_info):
        print('Adding new account...')
        data = {
            'name': acc_info['name'],
            'sicCode': acc_info['jib']
        }
        response = client.request('POST', 'Account', data)
        posted_account_id = response['id']
        posted_account_name = response['name']
        print(f'New account have been added: {posted_account_name}')
        return posted_account_id

    def check_account(pdf_data):
        # provjeri postoji li Pravno lice u CRM
        print('Checking if account already exists...')
        jib = pdf_data['uo']['jib']
        params = {
            "select": "name",
            "where": [
                {
                    "type": "equals",
                    "attribute": "sicCode",
                    "value": f'{jib}',
                },
            ],
        }
        response = client.request('GET', 'Account', params)

        # ako ne postoji dodaj novo Pravno lice i vrati ID
        if response['total'] == 0:
            print('Account does not exist.')
            posted_account_id = post_account(pdf_data['uo'])
            return posted_account_id
        # ako postoji vrati ID
        else:
            print('Account:' ,response['list'][0]['name'])
            return response['list'][0]['id']
    
    def post_tender(pdf_data):
        print('Adding new tender...', datetime.now())
        data = pdf_data['osnovni_podaci']
        data['accounts1Id'] = account_id
        data['tipTendera'] = "Objavljeni"
        data['createdAt'] = json.dumps(datetime.now(), indent=4, default=str)
        response = client.request('POST', 'Tenderi', data)
        tender_id = response['id']
        print('New tender have been successfully added!')
        return tender_id


    def post_document(file_path, tender_id):
    # post attachment
        print('Adding new document...')
        print('    - Adding new attachment...')
        with open(file_path, "rb") as pdf_file:
            encoded_file = base64.b64encode(pdf_file.read()).decode()
            regex_query = re.compile('(?<=watch_folder\/).*')
            file_name = regex_query.findall(file_path)[0]
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

        print('    - Adding new document...')
        data = {
            "name": f"{file_name}",
            "fileId": doc_id,
            "publishDate": publish_date,
            "status": "Active",
            "tenderisIds": [f"{tender_id}"],
            "folderId": "62552a7b40dcbca04"
            }
        client.request('POST', 'Document', data)
        print('New document have been successfully added!')

    account_id = check_account(pdf_data)
    tender_id = post_tender(pdf_data)
    post_document(file_path, tender_id)


