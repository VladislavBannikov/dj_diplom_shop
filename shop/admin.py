from django.contrib import admin

from .models import Order, OrderItems, Product, Section
from django import forms


class SectionAdminForm(forms.ModelForm):
    def clean_parent(self):
        parent = self.cleaned_data.get("parent", None)
        if parent:
            if parent.level > 0:
                raise forms.ValidationError("Only two-level menu is allowed")
        return parent


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    form = SectionAdminForm
    fields = ("name", "parent", "slug")
    readonly_fields = ("slug",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'section', 'price',)
    list_editable = ('price',)
    list_filter = ('section',)
    # TODO: need validation of Section that is only leaf (isn't root)


class OrderItemsAdmin(admin.TabularInline):
    model = OrderItems
    fields = ("product", "count")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("user", "date", "items_count", "order_price")
    ordering = ("-date",)

    inlines = [OrderItemsAdmin, ]

    # to rename column in list view. Called get_items_count of Order object. Name to display - "items count"
    def items_count(self, obj):
        return obj.get_items_count()
