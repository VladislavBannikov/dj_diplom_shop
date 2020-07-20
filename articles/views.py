from django.shortcuts import render

# Create your views here.


def articles_view(request):
    template = "articles/articles.html"

    # context = {"columns": COLUMNS, "table": table, "csv_file": CSV_FILENAME}
    result = render(request, template)
    return result