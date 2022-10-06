from django.apps import AppConfig


class FileSyncConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'file_sync'

    def ready(self):
        print('file sync...')