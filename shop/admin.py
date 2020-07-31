from django.contrib import admin

from .models import Order, OrderItems, Product, Section


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    fields = ("name", "parent", "slug")
    readonly_fields = ("slug",)
    # TODO: need Section.level validation (level=1 max)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'section')
    list_filter = ('section',)
    # TODO: need validation of Section that is only leaf (isn't root)


# @admin.register(OrderItems)
class OrderItemsAdmin(admin.TabularInline):
    model = OrderItems


# class OrderSumAdmin(admin.TabularInline):
#     # model = ["sdf","sdf"]
#     model = None
#     pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("user", "date", "items_count")
    ordering = ("-date",)

    inlines = [OrderItemsAdmin, ]


    # to rename column in list view. Called get_items_count of Order object. Name to display - "items count"
    def items_count(self, obj):
        return obj.get_items_count()
