from django.shortcuts import render
from main.models import ShippingAddress
from shop.utils import *

# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from main.models import Users
from .models import Product, Cart, Wishlist, Order, Order_items
from django.db.models import Q, Count
from django.core import serializers

from django.core.paginator import Paginator
import razorpay


# Create your views here.
def search(request, search_text):
    products = Product.objects.filter(
        Q(product_name__icontains=search_text) | Q(product_category__icontains=search_text) | Q(
            product_type__icontains=search_text) | Q(product_brand__icontains=search_text))
    return JsonResponse(serializers.serialize('json', products), safe=False)


def shop(request, cat_type="All", category="All"):
    if cat_type == 'All' and category == 'All':
        all_products = Product.objects.filter(status='In Stock')
    elif cat_type != 'All' and category == 'All':
        all_products = Product.objects.filter(product_type=cat_type, status='In Stock')
    elif cat_type != 'All' and category != 'All':
        all_products = Product.objects.filter(product_type=cat_type, product_category=category, status='In Stock')

    items_per_page = 6
    paginator = Paginator(all_products, items_per_page)
    page_number = request.GET.get('page')  # Get the current page number from the request
    page = paginator.get_page(page_number)

    categories_with_counts = Product.objects.values('product_type').annotate(product_count=Count('product_type'))
    data = {
        'type': cat_type,
        'product_categories':categories_with_counts,
        'category': category,
        'products': page
    }
    # print(request.session['cart_products'])
    return render(request, 'shop/shop_list.html', data)


def product_details(request, prod_id):
    cart_det=Cart.objects.filter(product_id=prod_id)
    if len(cart_det)>0:
        quantity=cart_det
    else:
        quantity=1
    product_det=Product.objects.get(id=prod_id)
    # featured products
    featured_products=fetch_featured_products(request)

    data={
        'featured_products':featured_products,
        'product':product_det,
        'quantity':quantity
    }
    return render(request, 'shop/product_details.html',data)


def view_cart(request):
    # featured products
    featured_products=fetch_featured_products(request)

    # deals of week
    deals_of_week=fetch_deals_of_week(request)
    cart_items = Cart.objects.filter(email_id=request.session['email_id'])
    data = {
        "cart_products": cart_items,
        'featured_products':featured_products,
        'deals_of_week':deals_of_week,
    }
    return render(request, 'shop/cart.html', data)


def add_to_cart(request, prod_id, quantity=1):
    user = Users.objects.get(email_id=request.session['email_id'])
    product = Product.objects.get(id=prod_id)
    Cart.objects.create(product_id=product, email_id=user, quantity=quantity)

    # fetching product ids as list from cart table and storing in session
    cart_product_ids = fetch_cart_ids(request)
    request.session['cart_ids'] = cart_product_ids

    previous_path = request.META.get('HTTP_REFERER', '/')
    return redirect(previous_path)


def remove_from_cart(request, prod_id):
    Cart.objects.filter(email_id=request.session['email_id'], product_id=prod_id).delete()

    # fetching product ids as list from cart table and storing in session
    cart_product_ids = fetch_cart_ids(request)
    request.session['cart_ids'] = cart_product_ids

    previous_path = request.META.get('HTTP_REFERER', '/')
    return redirect(previous_path)


def update_cart(request, cart_id, quantity):
    Cart.objects.filter(id=cart_id).update(quantity=quantity)
    fetch_cart_ids(request)
    return HttpResponse(request.session['cart_total_price'])


def add_to_wishlist(request, prod_id):
    user = Users.objects.get(email_id=request.session['email_id'])
    product = Product.objects.get(id=prod_id)
    Wishlist.objects.create(product_id=product, email_id=user)

    # fetching product ids as list from wishlist table and storing in session
    wish_product_ids = fetch_wish_ids(request)
    request.session['wish_ids'] = wish_product_ids

    previous_path = request.META.get('HTTP_REFERER', '/')
    return redirect(previous_path)


def remove_from_wishlist(request, prod_id):
    Wishlist.objects.filter(email_id=request.session['email_id'], product_id=prod_id).delete()

    # fetching product ids as list from wishlist table and storing in session
    wish_product_ids = fetch_wish_ids(request)
    request.session['wish_ids'] = wish_product_ids

    previous_path = request.META.get('HTTP_REFERER', '/')
    return redirect(previous_path)


def view_wishlist(request):
    # featured products
    featured_products=fetch_featured_products(request)

    # deals of week
    deals_of_week=fetch_deals_of_week(request)
    wishlist_products = Wishlist.objects.filter(email_id=request.session['email_id'])
    data = {
        'wishlist_products': wishlist_products,
        'featured_products':featured_products,
        'deals_of_week':deals_of_week,
    }
    return render(request, 'shop/wishlist.html', data)


def view_product(request, product_id):
    product_details = Product.objects.values().get(id=product_id)
    return JsonResponse(product_details)

def checkout(request):
    adresses=ShippingAddress.objects.filter(email_id=request.session['email_id'])
    cart_items = Cart.objects.filter(email_id=request.session['email_id'])
    data={
        'addresses':adresses,
        "cart_products": cart_items
    }
    default_address=ShippingAddress.objects.filter(email_id=request.session['email_id'],default_address=True)
    if default_address:
        data['default_address_id']=default_address[0].id
    return render(request,'shop/checkout.html',data)

def placeorder(request):
    ship_id=request.POST.get('ship_id')
    total_price=request.POST.get('total_price')
    #razerpay instance
    client = razorpay.Client(auth=('rzp_test_k80E4Xds9GhX2n', 'IoR7NNrM1Mqy2r9GtoObQX7X'))
    data = {"amount": float(total_price)*100, "currency": "INR"}
    order_details = client.order.create(data=data)

    user=Users.objects.get(email_id=request.session['email_id'])
    shipping_add=ShippingAddress.objects.get(id=ship_id)
    order_data=Order.objects.create(order_id=order_details['id'],email_id=user,total_amount=total_price,shipping_address=shipping_add)
    cart_items = Cart.objects.filter(email_id=request.session['email_id'])
    for item in cart_items:
        price=item.product_id.discount_price()
        Order_items.objects.create(order_id=order_data,product_id=item.product_id,price=price,quantity=item.quantity)
    data={
        'order_details':order_details,
        'user':user
    }
    return render(request,'shop/processing.html',data)

def order_success(request):
    Cart.objects.filter(email_id=request.session['email_id']).delete()
    # fetching product ids as list from cart table and storing in session
    cart_product_ids = fetch_cart_ids(request)
    request.session['cart_ids'] = cart_product_ids
    return render(request,'shop/order_success.html')

def fetch_order(request,order_id):
    order_details=Order_items.objects.get(id=order_id)
    data={
        'order_id':order_details.order_id.order_id,
        'product_name':order_details.product_id.product_name,
        'quantity':order_details.quantity,
        'price':order_details.price,
        'total_price':order_details.order_id.total_amount,
        'product_image':order_details.product_id.image.url,
        'order_date':order_details.order_id.formatted_order_date()
    }
    return JsonResponse(data)