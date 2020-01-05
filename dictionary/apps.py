from django.apps import AppConfig


class DictionaryConfig(AppConfig):
    name = 'dictionary'

    def ready(self):
        from .signals import handlers
