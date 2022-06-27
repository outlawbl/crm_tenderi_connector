import re
import os
import time
import shutil
import pathlib
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

if __name__ == "__main__":
    patterns = ["*"]
    ignore_patterns = None
    ignore_directories = True
    case_sensitive = True
    my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)

def on_created(event):
    time.sleep(3)
    print(f"{event.src_path} je kreiran!")
    file_path = event.src_path
    dir_path = os.path.dirname(os.path.realpath(file_path))
    rel_dir_path = os.path.basename(dir_path)
    file_name = pathlib.Path(file_path).name
    file_extention = pathlib.Path(file_path).suffix
    print(file_extention)
    shutil.copyfile(file_path, f'./uploads_from_remote_server/{file_name}')

def on_deleted(event):
    print(f"{event.src_path} je obrisan!")
    pass

def on_modified(event):
    # print(f"{event.src_path} je promjenjen!")
    pass
    
def on_moved(event):
    # time.sleep(1)
    print(f"{event.src_path} je promjenjen u {event.dest_path}")
   

my_event_handler.on_created = on_created
my_event_handler.on_deleted = on_deleted
my_event_handler.on_modified = on_modified
my_event_handler.on_moved = on_moved

path = ["./watch_folder", "./watch_folder2"]
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

