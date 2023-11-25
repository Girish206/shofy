from django.urls import path
from main import views

urlpatterns = [
    path('', views.main_index),
    path('register/', views.reg_index),
    path('login/', views.login),
    path('about/', views.about),
    path('logout/', views.logout),
    path('contact/', views.contact),
    path('account/', views.my_account),
    path('account/profile/', views.profile),
    path('account/shipping_address/', views.shipping_address),
    path('account/shipping_address/new/', views.new_shipping_address),
    path('account/shipping_address/edit/<ship_id>/', views.update_shipping_address),
    path('account/shipping_address/remove/<ship_id>/', views.remove_shipping_address),
    path('account/shipping_address/set_default/<ship_id>/', views.set_as_default),
    path('account/shipping_address/get/<ship_id>/', views.get_shipping_address),
    path('account/my_orders/',views.my_orders),
]
