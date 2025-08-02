from django.apps import AppConfig

class YourAppConfig(AppConfig):
    name = 'core'

    def ready(self):
        import core.signals

