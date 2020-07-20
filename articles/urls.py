from django.urls import path

from .views import articles_view

urlpatterns = [
    path("", articles_view, name="articles_view"),

]