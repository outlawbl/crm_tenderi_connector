import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from readPdf import readPdf
from espo_api_client import EspoAPI
from main import main_function
import re
import os

client = EspoAPI('http://10.0.0.192', '3a6e01aeee51af096936fe7c6eb4dd06')

if __name__ == "__main__":
    patterns = ["*"]
    ignore_patterns = None
    ignore_directories = False
    case_sensitive = True
    my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)

def on_created(event):
    print(f"{event.src_path} je kreiran!")
    file_path = event.src_path
    dir_path = os.path.dirname(os.path.realpath(file_path))
    # file_extention_re = re.compile('^.*\.(jpg|JPG|gif|GIF|doc|DOC|pdf|PDF)$')
    # file_extention_re = re.compile('(\\.[^.]+)$')
    file_name = re.compile('(?<=folder/).*(?=\.)').findall(file_path)[0]
    file_extention = re.compile('([^.]+)$').findall(file_path)[0]
    try:
        global pdf_data 
        pdf_data = readPdf(f"{event.src_path}")
        print(pdf_data, file_path)
        main_function(pdf_data, file_path)
        new_file_name = f'_synced_{file_name}.{file_extention}'
        os.rename(file_path, os.path.join(dir_path, new_file_name))
    except:
        print('Fajl nije ispravan!', file_extention)

    # print(client.request('POST', 'Tenderi', pdf_data['osnovni_podaci']))

def on_deleted(event):
    # print(f"{event.src_path} je obrisan!")
    pass

def on_modified(event):
    # print(f"{event.src_path} je promjenjen!")
    pass
    
def on_moved(event):
    # print(f"{event.src_path} je promjenjen u {event.dest_path}")
    pass


my_event_handler.on_created = on_created
my_event_handler.on_deleted = on_deleted
my_event_handler.on_modified = on_modified
my_event_handler.on_moved = on_moved

path = "./watch_folder"
go_recursively = True
my_observer = Observer()
my_observer.schedule(my_event_handler, path, recursive=go_recursively)

my_observer.start()
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    my_observer.stop()
    my_observer.join()

