from django.apps import AppConfig


class StorylineConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.storyline'

    def ready(self):
        import apps.storyline.signals
