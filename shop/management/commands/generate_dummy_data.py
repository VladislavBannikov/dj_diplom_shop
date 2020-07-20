import os

import requests
from django.conf import settings
from django.core.management.base import BaseCommand

from shop.models import Product, Section

BASE_DIR = os.path.dirname(__file__)

base_name = "phone"
size = "200x300"
ext = "png"
count = 20


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):

        g = Section.objects.create(name='Gadgets')
        p = Section.objects.create(name='Phones', parent=g)

        for i in range(1, count):
            name = f'{base_name} {i}'

            response = requests.get(f"https://dummyimage.com/{size}/000000/fff.{ext}&text={name}")
            open(os.path.join(settings.MEDIA_ROOT, f'{base_name} {i}.{ext}'), 'wb').write(response.content)

            Product.objects.create(name=name,
                                   image=f"products/{name}.{ext}",
                                   description=f"{name} test description {name}",
                                   section=p,
                                   )
            print(name)
