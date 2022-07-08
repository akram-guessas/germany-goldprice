from django.apps import AppConfig


class GoldpriceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'goldprice'
    
    def ready(self):
        print("Starting Scheduler ...")
        from .goldprice_schedule import goldprice_updator
        goldprice_updator.start()
