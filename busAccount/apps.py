from django.apps import AppConfig

class BusAccountConfig(AppConfig):
    name = 'busAccount'

    def ready(self):
        import busAccount.signals

