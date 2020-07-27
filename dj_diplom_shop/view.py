# from django.shortcuts import redirect
# from django.urls import reverse
#
#
# def index(request):
#     return redirect(reverse())

from django.shortcuts import render

from articles.models import Article
from shop.models import Product


def main_page(request):
    template = "home_page.html"
    articles = Article.objects.all().order_by("-published_at")
    products = Product.objects.order_by('?')[:3]
    context = {"articles": articles,
               "products": products}
    result = render(request, template, context)
    return result
