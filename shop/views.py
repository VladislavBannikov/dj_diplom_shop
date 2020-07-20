from collections import Counter
from urllib.parse import urlencode, urlparse, urlunparse

from django.contrib.sessions.models import Session
from django.core.paginator import Paginator
from django.db.models import Sum
from django.shortcuts import redirect, render, render_to_response
from django.urls import reverse
from django.utils import timezone
from django.views import View

from .models import Cart, Order, OrderItems, Product, Section

PAGINATOR_ITEMS_PER_PAGE = 6

paginator_catalog_slug = ''
paginator = None


def catalog_view(request, catalog_slug):
    global paginator
    global paginator_catalog_slug
    template = "shop/catalog.html"
    section = Section.objects.get(slug=catalog_slug)

    if paginator_catalog_slug != catalog_slug:
        paginator = Paginator(section.products.all(), PAGINATOR_ITEMS_PER_PAGE)
        paginator_catalog_slug = catalog_slug

    cur_url = request.path

    current_page_number = request.GET.get('page', 1)
    current_page = paginator.get_page(current_page_number)
    current_page_number = current_page.number
    next_page_url = None
    prev_page_url = None

    if current_page.has_next():
        next_page_url = f'{cur_url}?page={current_page.next_page_number()}'

    if current_page.has_previous():
        prev_page_url = f'{cur_url}?page={current_page.previous_page_number()}'

    context = {
        'products': paginator.page(current_page_number).object_list,
        'section': section,
        'current_page': current_page_number,
        'prev_page_url': prev_page_url,
        'next_page_url': next_page_url,
    }

    return render(request, template_name=template, context=context)


def product_view(request, product_slug):
    template = "shop/product.html"
    context = {"product": Product.objects.get(slug=product_slug)}

    return render(request, template_name=template, context=context)


def cart_view(request):
    template = "shop/cart.html"

    session_key = request.session.session_key
    session = Session.objects.get(session_key=session_key)
    items = Cart.objects.filter(session=session).select_related('product')
    sum = items.aggregate(sum=Sum('count')).get('sum')
    context = {"items": items, 'sum': sum}

    return render(request, template_name=template, context=context)


class AddToCartView(View):
    # form_class = CalcForm
    # template_name = ""

    def post(self, request, *args, **kwargs):
        product_slug = request.POST.get('product_slug', None)

        session_key = request.session.session_key
        session = Session.objects.get(session_key=session_key)
        product = Product.objects.get(slug=product_slug)

        (product_in_cart, _) = Cart.objects.get_or_create(session=session, product=product)
        # if product_in_cart is None:
        #     product_in_cart = Cart(session=session, product=product, count=1)
        # else:
        product_in_cart.count += 1
        product_in_cart.save()

        page_number = request.POST.get('redirect_page', 1)
        red = redirect(f"{request.POST.get('redirect_url')}?page={page_number}")
        return red


class CreateOrderView(View):
    def post(self, request, *args, **kwargs):
        user = request.user
        date = timezone.now()
        order = Order.objects.create(user=user, date=date)

        session_key = request.session.session_key
        session = Session.objects.get(session_key=session_key)
        items = Cart.objects.filter(session=session)

        for item in items:
            OrderItems.objects.create(product=item.product,count=item.count,order=order)

        items.delete()
        red = redirect("/")
        return red
