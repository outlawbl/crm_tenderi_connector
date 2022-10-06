from django.apps import AppConfig
from crm_connector.settings import BASE_DIR
import configparser
import os
import pathlib
import logging
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer
import time
from watcher.main import main_function
from watcher.readPdf import readPdf


class WatcherConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'watcher'

    if os.environ.get('RUN_MAIN', None) != 'true':
        def ready(self):
            config = configparser.ConfigParser(converters={'list': lambda x: [i.strip() for i in x.split(',')]})
            data_file = os.path.join(BASE_DIR, 'config.ini')
            config.read(data_file)

            logging.basicConfig(filename=config['PATHS']['logPath'], level=logging.ERROR)
            patterns = ["*"]
            ignore_patterns = None
            ignore_directories = True
            case_sensitive = True
            my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)

            def on_created(event):
                time.sleep(3)
                print(f"{event.src_path} je kreiran!")
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