import re
import os
import time
import shutil
import pathlib
import logging
import configparser
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from readPdf import readPdf
from espo_api_client import EspoAPI
from crm_connector.settings import BASE_DIR
from main import main_function

config = configparser.ConfigParser(converters={'list': lambda x: [i.strip() for i in x.split(',')]})
data_file = os.path.join(BASE_DIR, 'config.ini')
config.read(data_file)

logging.basicConfig(filename=config['PATHS']['logPath'], level=logging.ERROR)

if __name__ == "__main__":
    patterns = ["*"]
    ignore_patterns = None
    ignore_directories = True
    case_sensitive = True
    my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)

def on_created(event):
    time.sleep(3)
    logging.info(f"{event.src_path} je kreiran!")
    file_path = event.src_path
    dir_path = os.path.dirname(os.path.realpath(file_path))
    file_extention = pathlib.Path(file_path).suffix
    print(file_extention)
    try:
        pdf_data = readPdf(file_path)
        main_function(pdf_data, file_path)
        
    except Exception as e:
        print('Greska:' ,e)
        logging.error(e)
        pass

def on_deleted(event):
    print(f"{event.src_path} je obrisan!")
    pass

def on_modified(event):
    # print(f"{event.src_path} je promjenjen!")
    pass
    
def on_moved(event):
    # time.sleep(1)
    print(f"{event.src_path} je promjenjen u {event.dest_path}")
    # file_path = event.dest_path
    # dir_path = os.path.dirname(os.path.realpath(file_path))
    # file_name = os.path.basename(file_path)
    # if file_name.startswith('_to_be_synced_'):
    #     try:
    #         global pdf_data 
    #         pdf_data = readPdf(file_path)
    #         print(pdf_data, file_path)
    #         main_function(pdf_data, file_path)
    #         new_file_name = f'_synced_{file_name[14::]}'
    #         new_file_path = os.path.join(dir_path, new_file_name)
    #         os.rename(file_path, new_file_path)

    #         new_path = os.path.join(dir_path, 'synced')
            
    #         # ako ne postoji folder "synced", napravi ga.
    #         if not os.path.exists(new_path):
    #             os.mkdir(new_path)

    #         # premjesti sinhronizovan fajl u "synced" folder
    #         shutil.move(new_file_path, os.path.join(new_path, new_file_name))
    #     except Exception as e: 
    #         print(e)
    #         pass
    # else:
    #     pass


my_event_handler.on_created = on_created
my_event_handler.on_deleted = on_deleted
my_event_handler.on_modified = on_modified
my_event_handler.on_moved = on_moved

watch_folder_path = config['PATHS']['watchFolderPath']

path = [watch_folder_path]
go_recursively = False
my_observer = Observer()
for i in path:
    my_observer.schedule(my_event_handler, i, recursive=go_recursively)

my_observer.start()
try:
    while True:
        time.sleep(3)
except KeyboardInterrupt:
    my_observer.stop()
    my_observer.join()
