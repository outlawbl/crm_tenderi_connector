import imp
from api import client, get_tender
from datetime import date, datetime
import base64
import pprint
import re
import json

def main_function(pdf_data, file_path):
    tender_broj_postupka = pdf_data['osnovni_podaci']['brojPostupka']
    total_tenders = get_tender(tender_broj_postupka)['total']
    print(total_tenders)
    if total_tenders == 0:
        if pdf_data['tip_dokumenta'] == '3':
            def post_account(acc_info):
                print(datetime.now().strftime("%H:%M:%S"), 'Adding new account...')
                data = {
                    'name': acc_info['name'],
                    'sicCode': acc_info['jib']
                }
                response = client.request('POST', 'Account', data)
                posted_account_id = response['id']
                posted_account_name = response['name']
                print(datetime.now().strftime("%H:%M:%S"), f'New account have been added: {posted_account_name}')
                return posted_account_id

            def check_account(pdf_data):
                # provjeri postoji li Pravno lice u CRM
                print(datetime.now().strftime("%H:%M:%S"), 'Checking if account already exists...')
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

                # ako ne postoji dodaj novo Pravno lice i vrati ID
                if response['total'] == 0:
                    print(datetime.now().strftime("%H:%M:%S"), 'Account does not exist.')
                    posted_account_id = post_account(pdf_data['uo'])
                    return posted_account_id
                # ako postoji vrati ID
                else:
                    print('Account:' ,response['list'][0]['name'])
                    return response['list'][0]['id']
            
            def post_tender(pdf_data):
                print(datetime.now().strftime("%H:%M:%S"), 'Adding new tender...')
                data = pdf_data['osnovni_podaci']
                data['accounts1Id'] = account_id
                data['tipTendera'] = "Objavljeni"
                data['createdAt'] = json.dumps(datetime.now(), indent=4, default=str)
                response = client.request('POST', 'Tenderi', data)
                tender_id = response['id']
                print(datetime.now().strftime("%H:%M:%S"), 'New tender have been successfully added!')
                return tender_id


            def post_document(file_path, tender_id):
            # post attachment
                print(datetime.now().strftime("%H:%M:%S"), 'Adding new document...')
                print(datetime.now().strftime("%H:%M:%S"), '    - Adding new attachment...')
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
                    "name": "Obavjestenje o nabavci",
                    "fileId": doc_id,
                    "publishDate": publish_date,
                    "status": "Active",
                    "tenderisIds": [f"{tender_id}"],
                    "folderId": "62552a7b40dcbca04"
                    }
                client.request('POST', 'Document', data)
                print('New document have been successfully added!')

            # if pdf_data
            account_id = check_account(pdf_data)
            tender_id = post_tender(pdf_data)
            post_document(file_path, tender_id)
        else:
            print('Dokument nije obavjestenje o nabavci!')
    else:
        print('Tender vec postoji!!!')