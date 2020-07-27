from django.shortcuts import render

# Create your views here.
from .models import Article


def articles_view(request):
    template = "articles/articles.html"

    # context = {"columns": COLUMNS, "table": table, "csv_file": CSV_FILENAME}
    result = render(request, template)
    return result


def article_view(request, article_slug):
    template = "articles/article.html"
    article = Article.objects.get(slug=article_slug)

    context = {"article": article}
    result = render(request, template, context)
    return result
