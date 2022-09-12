from django.http import HttpResponse
from main import main_function
from readPdf import readPdf
from api import get_document_fileId
import logging
from configparser import ConfigParser
import os

data_file = '/home/sandro/Dev/crm_tenderi_connector/crm_connector/config.ini'
config = ConfigParser()
config.read(data_file)

logging.basicConfig(filename=config['PATHS']['logPath'], level=logging.ERROR)


def create_tender(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def home(request):
    return HttpResponse("Home")

def test(request, document_id):
    try:
        upload_path = config['PATHS']['uploadFoderPath']
        fileId = get_document_fileId('Document', document_id)
        file_path = os.path.join(upload_path, fileId)
        pdf_data = readPdf(file_path)
        main_function(pdf_data, file_path)
        return HttpResponse("App runned")
        
    except Exception as e:
        return HttpResponse("Something went wrong")