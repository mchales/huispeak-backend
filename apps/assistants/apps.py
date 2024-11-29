from django.apps import AppConfig


class AssistantsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.assistants'

    def ready(self):
        import apps.assistants.signals