from django.apps import AppConfig

print("==========3")

class ShopConfig(AppConfig):
    name = 'shop'
    print("=============1")

    def ready(self):
        print("--------readt--------")
        import shop.signals.handlers #noqa