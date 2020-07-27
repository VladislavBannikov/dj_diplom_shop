import os

import requests
from django.conf import settings
from django.core.management.base import BaseCommand

from shop.models import Product, Section

BASE_DIR = os.path.dirname(__file__)


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        def generate(config):
            base_name = config.get("base_name")
            size = config.get("size")
            ext = config.get("ext")
            count = config.get("count")
            image_catalog = config.get("image_catalog")
            bg_color = config.get("bg_color")
            text_color = config.get("text_color")
            section_name = config.get("section_name")

            section = Section.objects.filter(name=section_name).first()

            for i in range(1, count):
                name = f'{base_name} {i}'

                response = requests.get(f"https://dummyimage.com/{size}/{bg_color}/{text_color}.{ext}&text={name}")
                open(os.path.join(settings.MEDIA_ROOT, image_catalog, f'{base_name} {i}.{ext}'), 'wb').write(
                    response.content)

                Product.objects.create(name=name,
                                       image=f"products/{name}.{ext}",
                                       description=f"{name} test description {name}",
                                       section=section,
                                       )
                print(name)

        gadgets = Section.objects.create(name='Gadgets')
        phones = Section.objects.create(name='Phones', parent=gadgets)
        watches = Section.objects.create(name='Phones', parent=gadgets)

        accessories = Section.objects.create(name='Accessories')
        phones = Section.objects.create(name='Watch stripes', parent=accessories)
        watches = Section.objects.create(name='Phone cases', parent=accessories)

        conf = [
            {
                "base_name": "phone",
                "size": "200x300",
                "ext": "png",
                "count": 20,
                "image_catalog": "products",
                "bg_color": 'bd55bd',
                "text_color": 'fff',
                "section_name": 'Phones'
            },
            {
                "base_name": "watch",
                "size": "200x300",
                "ext": "png",
                "count": 3,
                "image_catalog": "products",
                "bg_color": 'bd55bd',
                "text_color": 'fff',
                "section_name": 'Watches'
            },
            {
                "base_name": "case",
                "size": "200x300",
                "ext": "png",
                "count": 30,
                "image_catalog": "products",
                "bg_color": '60717d',
                "text_color": 'fff',
                "section_name": 'Phone cases'
            },
            {
                "base_name": "stripe",
                "size": "200x300",
                "ext": "png",
                "count": 15,
                "image_catalog": "products",
                "bg_color": 'e81c1c',
                "text_color": 'fff',
                "section_name": 'Watch stripes'
            }
        ]
        for i in conf:
            generate(i)

        #
        # for i in range(1, count):
        #     name = f'{base_name} {i}'
        #
        #     response = requests.get(f"https://dummyimage.com/{size}/000000/fff.{ext}&text={name}")
        #     open(os.path.join(settings.MEDIA_ROOT, f'{base_name} {i}.{ext}'), 'wb').write(response.content)
        #
        #     Product.objects.create(name=name,
        #                            image=f"products/{name}.{ext}",
        #                            description=f"{name} test description {name}",
        #                            section=phones,
        #                            )
        #     print(name)
