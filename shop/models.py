from ckeditor.fields import RichTextField
from django.contrib.sessions.models import Session
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Sum, F, FloatField
from django.template.defaultfilters import slugify
from mptt.models import MPTTModel, TreeForeignKey

from registration.models import User


class Section(MPTTModel):
    name = models.CharField(max_length=255, blank=False, unique=True, verbose_name="Section name")
    slug = models.SlugField(max_length=255, blank=True, unique=True, verbose_name='Slug')
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Section, self).save(*args, **kwargs)

    def __str__(self):
        return self.slug


class Product(models.Model):
    name = models.CharField(max_length=255, blank=False, verbose_name="Name")
    image = models.ImageField(upload_to="products", verbose_name="Picture")
    price = models.FloatField(blank=False, verbose_name='Price')
    # stock = models.PositiveIntegerField(default=0, verbose_name='Count in stock')
    description = RichTextField(verbose_name="Description")
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name="products")
    slug = models.SlugField(max_length=255, blank=True, unique=True, verbose_name='Slug')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Cart(models.Model):
    pass


#     session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name="cart")
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="cart")
#     count = models.PositiveIntegerField(default=0, null=False, verbose_name='Count')


class OrderItems(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="order_item")
    count = models.PositiveIntegerField(default=0, null=False, verbose_name='Count')
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name="items")


class Order(models.Model):
    date = models.DateField(null=False, verbose_name="Order date")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Customer')
    order_price = models.FloatField(default=0, verbose_name="Order price")

    def __str__(self):
        return f"{self.user.email} - {self.date}"

    def get_items_count(self):
        return self.items.aggregate(sum=Sum('count')).get('sum')

    def calc_order_price(self):
        self.order_price = self.items.aggregate(total=Sum(F('count') * F('product__price'), output_field=FloatField()))[
            'total'] or 0
        self.save()
        return None
