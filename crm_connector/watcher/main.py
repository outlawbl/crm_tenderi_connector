import logging
from .api import client, get_documents, get_tender, get_account, post_account, post_tender, post_document, get_document, get_document_fileId, update_tender_documents
from datetime import date, datetime
from crm_connector.settings import BASE_DIR
from configparser import ConfigParser
import base64
import pprint
import re
import json
import os

data_file = '/home/sandro/Dev/crm_tenderi_connector/crm_connector/config.ini'
config = ConfigParser()
config.read(data_file)

logging.basicConfig(filename=config['PATHS']['logPath'], format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)

def main_function(pdf_data, file_path):
    if 'tip_dokumenta' in pdf_data:
        # Da li je dokument Obavjestenje o nabavci
        if pdf_data['tip_dokumenta'] == '3':
            # Provjeri postoji li vec taj tender
            total_tenders = get_tender(pdf_data['osnovni_podaci']['brojPostupka'])

            # Ako ne postoji tender sa tim brojem postupka, dodaj ga
            if total_tenders['total'] == 0:
                file_name = os.path.basename(file_path)

                # provjeri postoji li Pravno lice u CRM
                fetched_account_data = get_account(pdf_data)

                # ako ne postoji dodaj novo Pravno lice i vrati ID
                if fetched_account_data['total'] == 0:
                    logging.info('Account does not exist.')
                    account_id = post_account(pdf_data['uo'])
                    # return account_id

                # ako postoji Pravno lice vrati ID
                else:
                    print('Account:' ,fetched_account_data['list'][0]['name'])
                    account_id = fetched_account_data['list'][0]['id']

                # Dodaj novi tender
                tender_id = post_tender(pdf_data, account_id)

                # Dohvati trenutne dokumente na tenderu
                tender_documents_ids = []
                tender_documents_ids = get_documents('Tenderi', tender_id)

                # Dohvati novi dokument
                new_document_id = get_document('fileId', file_name)
                # Dodaj ga postojecim
                tender_documents_ids.append(new_document_id)
                update_tender_documents(tender_id, tender_documents_ids)

            # Ako postoji tender loguj da postoji
            else:
                existed_tender = total_tenders['list'][0]['brojPostupka']
                logging.info(f'Tender vec postoji! {existed_tender}')
        else:
            print('Dokument nije validan')