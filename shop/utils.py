from django.db.models.functions import Random
from shop.models import Cart, Wishlist, Product
from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password, make_password
from django.contrib import messages
from shop.utils import *
from shop.models import *
from .models import *
from random import sample
import os
from django.db.models.functions import Random
from django.db.models import Sum

def fetch_cart_ids(request):
    cart_ids = Cart.objects.filter(email_id=request.session['email_id']).values_list('product_id', flat=True)
    cart_product_ids = []
    for obj in cart_ids:
        cart_product_ids.append(obj)

    fetch_cart_products(request)
    return cart_product_ids


def fetch_wish_ids(request):
    wish_ids = Wishlist.objects.filter(email_id=request.session['email_id']).values_list('product_id', flat=True)
    wish_product_ids = []
    for obj in wish_ids:
        wish_product_ids.append(obj)
    return wish_product_ids


def fetch_cart_products(request):
    cart_products = list(Cart.objects.filter(email_id=request.session['email_id']))
    cart_data = []
    total_cost = 0
    for cart_product in cart_products:
        total_cost += float(cart_product.product_id.discount_price()) * cart_product.quantity
        data = {
            'cart_id': cart_product.id,
            'product_id': cart_product.product_id.id,
            'product_name': cart_product.product_id.product_name,
            'product_type': cart_product.product_id.product_type,
            'product_category': cart_product.product_id.product_category,
            'product_brand': cart_product.product_id.product_brand,
            'price': float(cart_product.product_id.price),  # Convert Decimal to float
            'discounted_price': float(cart_product.product_id.discount_price()),  # Convert Decimal to float
            'quantity': cart_product.quantity,
            'image_url': cart_product.product_id.image.url,
            # Include other fields you need
        }
        cart_data.append(data)

    request.session['cart_total_price'] = total_cost
    request.session['cart_products'] = cart_data


def fetch_featured_products(request):
    all_products=Product.objects.filter(status='In Stock').exclude(discount=0)
    num_random_rows = min(8, len(all_products))
    featured_products = all_products.order_by(Random())[:num_random_rows]
    return featured_products


def fetch_deals_of_week(request):
    # Calculate the start and end date of the current week
    current_week_start = timezone.now().date() - timezone.timedelta(days=timezone.now().weekday())
    current_week_end = current_week_start + timezone.timedelta(days=6)
    print(current_week_start,current_week_end)
    # Get all products from orders placed this week
    order_item_ids = Order_items.objects.filter(order_id__order_date__range=[current_week_start, current_week_end]).values_list('product_id__id', flat=True).distinct()

    # Get the product objects for the selected product IDs
    all_products_of_week = Product.objects.filter(id__in=order_item_ids)

    # Determine the number of random rows to select (maximum of 6)
    num_random_rows = min(6, len(all_products_of_week))

    # Get a random selection of products
    deals_of_week = sample(list(all_products_of_week), num_random_rows)
    return deals_of_week