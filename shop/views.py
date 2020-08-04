from django.core.paginator import Paginator
from django.shortcuts import redirect, render

from django.utils import timezone
from django.views import View

from .models import Order, OrderItems, Product, Section

PAGINATOR_ITEMS_PER_PAGE = 6


def catalog_view(request, catalog_slug):
    template = "shop/catalog.html"
    section = Section.objects.get(slug=catalog_slug)
    sections = section.get_descendants(include_self=True)

    paginator = Paginator(Product.objects.filter(section__in=sections), PAGINATOR_ITEMS_PER_PAGE)

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

    # cart is a dict with key=product_slug and value=count
    cart = dict(request.session.get('cart', {}))

    sum_items = sum(cart.values())
    selected_products = Product.objects.filter(slug__in=cart.keys())
    # add product_name to the cart variable
    order_sum = 0
    for p in selected_products:
        order_sum += p.price * cart[p.slug]
        cart[p.slug] = {"product_name": p.name, "product_price": p.price, "count": cart[p.slug]}

    context = {"items": cart, 'sum': order_sum}

    return render(request, template_name=template, context=context)


class AddToCartView(View):

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
                OrderItems.objects.create(product=Product.objects.get(slug=product_in_cart_slug), count=count,
                                          order=order)

            order.calc_order_price()
            request.session['cart'] = {}

        red = redirect("/")
        return red
