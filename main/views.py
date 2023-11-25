from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password, make_password
from django.contrib import messages
from shop.utils import *
from shop.models import *
from .models import *
import os
from django.db.models.functions import Random
from django.db.models import Sum


# Create your views here.
def main_index(request):
    # featured products
    featured_products=fetch_featured_products(request)

    # deals of week
    deals_of_week=fetch_deals_of_week(request)

    data={
        'featured_products':featured_products,
        'deals_of_week':deals_of_week,
    }
    return render(request, 'home.html',data)


def reg_index(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')
        password = make_password(request.POST.get('password'))
        res = Users.objects.filter(email_id=email)
        if len(res) > 0:
            messages.warning(request, "User already exist!")
            return render(request, "auth/register.html")
        else:
            Users.objects.create(name=name, email_id=email, mobile_number=mobile,password=password)
            request.session['name'] = name
            request.session['email_id'] = email

            # fetching product ids as list from cart table and storing in session
            cart_product_ids = fetch_cart_ids(request)
            request.session['cart_ids'] = cart_product_ids
            # fetching product ids as list from wishlist table and storing in session
            wish_product_ids = fetch_wish_ids(request)
            request.session['wish_ids'] = wish_product_ids

            return redirect('/')

    else:
        return render(request, 'auth/register.html')


def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        res = Users.objects.filter(email_id=email)
        if len(res) == 0:
            messages.warning(request, "Invalid Email ID!")
            return redirect('/login')
        elif check_password(password, res[0].password):
            request.session['email_id'] = res[0].email_id
            request.session['name'] = res[0].name
            # storing image in session
            if res[0].photo:
                request.session['user_image'] = res[0].photo.url
            # fetching product ids as list from cart table and storing in session
            cart_product_ids = fetch_cart_ids(request)
            request.session['cart_ids'] = cart_product_ids
            # fetching product ids as list from wishlist table and storing in session
            wish_product_ids = fetch_wish_ids(request)
            request.session['wish_ids'] = wish_product_ids
            return redirect('/')
        else:
            messages.warning(request, "Invalid Password")
            return redirect('/login')
    else:
        return render(request, 'auth/login.html')


def about(request):
    return render(request, 'about.html')


def contact(request):
    if request.method=='POST':
        first_name=request.POST.get('firstname')
        last_name=request.POST.get('lastname')
        mobile_number=request.POST.get('mobile')
        email=request.POST.get('email')
        message=request.POST.get('message')
        ContactUs.objects.create(first_name=first_name,last_name=last_name,mobile_number=mobile_number,email_id=email,message=message)
        messages.success(request,'Feedback Submitted successfully')
        return redirect('/contact')
    return render(request, 'contact.html')


def logout(request):
    request.session.clear()
    return redirect('/')


def my_account(request):
    orders = Order.objects.filter(email_id=request.session['email_id']).count()
    wishlist_count = Wishlist.objects.filter(email_id=request.session['email_id']).count()
    cart_count = Cart.objects.filter(email_id=request.session['email_id']).count()
    data = {
        'orders_count': orders,
        'wishlist_count': wishlist_count,
        'cart_count': cart_count
    }
    return render(request, 'user/account.html', data)


def profile(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        user = Users.objects.get(email_id=email)
        user.name = name
        user.mobile_number = mobile
        if 'photo' in request.FILES:
            # deleteing exsisting photo from folder
            if user.photo:
                os.remove(user.photo.path)
            user.photo = request.FILES['photo']  # Assign the uploaded photo
            user.save()
            request.session['user_image'] = user.photo.url
        else:
            user.save()
        request.session['name']=name
        messages.success(request, 'Profile Updated Successfully')
        return redirect('/account/profile')
    else:
        user_data = Users.objects.get(email_id=request.session['email_id'])
        data = {
            'user': user_data
        }
        return render(request, 'user/profile.html', data)


def shipping_address(request):
    adresses=ShippingAddress.objects.filter(email_id=request.session['email_id'])
    data={
        'addresses':adresses
    }
    return render(request, 'user/address.html',data)


def new_shipping_address(request):
    name = request.POST.get('name')
    house_no = request.POST.get('house_no')
    mobile = request.POST.get('mobile')
    area = request.POST.get('area')
    landmark = request.POST.get('landmark')
    pincode = request.POST.get('pincode')
    city = request.POST.get('city')
    state = request.POST.get('state')
    # user details
    email_id = Users.objects.get(email_id=request.session['email_id'])

    adress_data=ShippingAddress.objects.create(name=name, email_id=email_id, mobile_number=mobile, house_no=house_no, area=area,
                                   landmark=landmark, pincode=pincode, city=city, state=state)
    if request.POST.get('default'):
        adress_data.default_address=True
        adress_data.save()
        ShippingAddress.objects.filter(email_id=request.session['email_id']).exclude(id=adress_data.id).update(default_address=False)
    previous_path = request.META.get('HTTP_REFERER', '/')
    return redirect(previous_path)

def update_shipping_address(request,ship_id):
    name = request.POST.get('name')
    house_no = request.POST.get('house_no')
    mobile = request.POST.get('mobile')
    area = request.POST.get('area')
    landmark = request.POST.get('landmark')
    pincode = request.POST.get('pincode')
    city = request.POST.get('city')
    state = request.POST.get('state')
    ShippingAddress.objects.filter(id=ship_id).update(name=name, mobile_number=mobile, house_no=house_no, area=area,
                                   landmark=landmark, pincode=pincode, city=city, state=state)
    messages.success(request,'Shipping Address Updated Successfully')
    previous_path = request.META.get('HTTP_REFERER', '/')
    return redirect(previous_path)

def remove_shipping_address(request,ship_id):
    ShippingAddress.objects.filter(id=ship_id).delete()
    previous_path = request.META.get('HTTP_REFERER', '/')
    return redirect(previous_path)

def set_as_default(request,ship_id):
    ShippingAddress.objects.filter(id=ship_id).update(default_address=True)
    ShippingAddress.objects.filter(email_id=request.session['email_id']).exclude(id=ship_id).update(default_address=False)
    previous_path = request.META.get('HTTP_REFERER', '/')
    return redirect(previous_path)

def get_shipping_address(request,ship_id):
    adress=ShippingAddress.objects.get(id=ship_id)
    return JsonResponse(model_to_dict(adress))


def my_orders(request):
    order = Order.objects.filter(email_id=request.session['email_id']).prefetch_related('order_items')
    data={
        'orders':order
    }
    return render(request,'user/my_orders.html',data)