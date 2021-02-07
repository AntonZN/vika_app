from django.apps import AppConfig


class MainConfig(AppConfig):
    name = 'vika_app.main'

    def ready(self):
        from vika_app.main import signals