import logging
from api import client, get_tender, get_account, post_account, post_tender, post_document
from datetime import date, datetime
import base64
import pprint
import re
import json

logging.basicConfig(filename='example.log', format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)

def main_function(pdf_data, file_path):
    if 'tip_dokumenta' in pdf_data:
        # Da li je dokument Obavjestenje o nabavci
        if pdf_data['tip_dokumenta'] == '3':
            # Provjeri postoji li vec taj tender
            total_tenders = get_tender(pdf_data['osnovni_podaci']['brojPostupka'])

            # Ako ne postoji tender sa tim brojem postupka, dodaj ga
            if total_tenders['total'] == 0:

                # provjeri postoji li Pravno lice u CRM
                fetched_account_data = get_account(pdf_data)

                # ako ne postoji dodaj novo Pravno lice i vrati ID
                if fetched_account_data['total'] == 0:
                    logging.info('Account does not exist.')
                    account_id = post_account(pdf_data['uo'])
                    # return account_id

                # ako postoji vrati ID
                else:
                    print('Account:' ,fetched_account_data['list'][0]['name'])
                    account_id = fetched_account_data['list'][0]['id']

                tender_id = post_tender(pdf_data, account_id)
                post_document(file_path, tender_id)
            else:
                logging.info(f'Tender vec postoji!', total_tenders['list'][0]['brojPostupka'])
        else:
            print('Dokument nije validan')