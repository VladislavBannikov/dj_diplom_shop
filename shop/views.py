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

    context = {
        'section': section,
    }

    if paginator.num_pages > 1:
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

        context.update({
            'products': paginator.page(current_page_number).object_list,
            'current_page': current_page_number,
            'prev_page_url': prev_page_url,
            'next_page_url': next_page_url,
        })
    else:
        context.update({
            'products': paginator.page(1).object_list,
        })

    return render(request, template_name=template, context=context)


def product_view(request, product_slug):
    template = "shop/product.html"
    context = {"product": Product.objects.get(slug=product_slug)}

    return render(request, template_name=template, context=context)


def cart_view(request):
    template = "shop/cart.html"

    # session_key = request.session.session_key
    # session = Session.objects.get(session_key=session_key)
    # items = Cart.objects.filter(session=session).select_related('product')
    # sum = items.aggregate(sum=Sum('count')).get('sum')
    # sum = 0

    cart = dict(request.session.get('cart', {}))
    sum_items = sum(cart.values())
    items = Product.objects.filter(slug__in=cart.keys())
    # TODO: what is the best way to add count from session cart to above QuerySet?

    context = {"items": items, 'sum': sum_items}

    return render(request, template_name=template, context=context)


class AddToCartView(View):
    # form_class = CalcForm
    # template_name = ""

    def post(self, request, *args, **kwargs):
        product_slug = request.POST.get('product_slug', None)

        cart = request.session.get('cart', {})
        product_current_count = cart.get(product_slug, 0)
        cart.update({product_slug: product_current_count + 1})
        request.session['cart'] = cart
        request.session.modified = True

        page_number = request.POST.get('redirect_page', 1)
        red = redirect(f"{request.POST.get('redirect_url')}?page={page_number}")
        return red


class CreateOrderView(View):
    def post(self, request, *args, **kwargs):
        cart = dict(request.session.get('cart', {}))
        if cart:

            user = request.user
            date = timezone.now()
            order = Order.objects.create(user=user, date=date)

            for product_in_cart_slug, count in cart.items():
                OrderItems.objects.create(product=Product.objects.get(slug=product_in_cart_slug), count=count, order=order)

            request.session['cart'] = {}

        red = redirect("/")
        return red
