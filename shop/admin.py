from django.contrib import admin

from .models import Order, OrderItems, Product, Section


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    fields = ("name", "parent", "slug")
    readonly_fields = ("slug",)
    # TODO: need Section.level validation (level=1 max)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'section', 'price', )
    list_editable = ('price', )
    list_filter = ('section',)
    # TODO: need validation of Section that is only leaf (isn't root)


# @admin.register(OrderItems)
class OrderItemsAdmin(admin.TabularInline):
    model = OrderItems
    fields = ("product", "count")


# class OrderSumAdmin(admin.TabularInline):
#     # model = ["sdf","sdf"]
#     model = None
#     pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("user", "date", "items_count", "order_price")
    ordering = ("-date",)

    inlines = [OrderItemsAdmin, ]

    # to rename column in list view. Called get_items_count of Order object. Name to display - "items count"
    def items_count(self, obj):
        return obj.get_items_count()

    def save_model(self, request, obj, form, change):

        super().save_model(request, obj, form, change)
        obj.calc_order_price()
        super().save_model(request, obj, form, change)
        # obj.save()
        #TODO: calculate order_price when order items have changed

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)

