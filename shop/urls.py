from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import (AddToCartView, CreateOrderView, cart_view, catalog_view,
                    product_view)

urlpatterns = [
    path("catalog/<slug:catalog_slug>/", catalog_view, name="catalog_view"),
    path("cart/", cart_view, name="cart_view"),
    path("add_to_cart/", AddToCartView.as_view(), name="add_to_cart_view"),
    path("create_order/", CreateOrderView.as_view(), name="create_order_view"),

    path("item/<slug:product_slug>", product_view, name="product_view"),

]