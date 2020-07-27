from django.urls import path

from .views import article_view, articles_view

urlpatterns = [
    # path("", articles_view, name="articles_view"),
    path("<slug:article_slug>/", article_view, name="article_view"),
]



# urlpatterns = [
#
#     path("cart/", cart_view, name="cart_view"),
#     path("add_to_cart/", AddToCartView.as_view(), name="add_to_cart_view"),
#     path("create_order/", CreateOrderView.as_view(), name="create_order_view"),
#
#     path("item/<slug:product_slug>", product_view, name="product_view"),
#
# ]