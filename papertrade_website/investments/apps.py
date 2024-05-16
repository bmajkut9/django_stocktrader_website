from django.apps import AppConfig


class InvestmentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'investments'
    
    def ready(self):
        import investments.signals

