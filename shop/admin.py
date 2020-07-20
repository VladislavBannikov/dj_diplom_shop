from django.contrib import admin

from .models import Product, Section


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ("name",)
    # readonly_fields = ["slug"]



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    pass
