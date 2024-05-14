from django.apps import AppConfig


class EventScheduleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.event_schedule'
    
    def ready(self) -> None:
        import apps.event_schedule.signals
