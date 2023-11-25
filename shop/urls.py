from django.urls import path

from shop import views

urlpatterns = [
    path('view/', views.shop),
    path('search/<search_text>/', views.search),
    path('product/view/<product_id>/', views.view_product),
    path('view/<cat_type>/', views.shop),
    path('view/<cat_type>/<category>/', views.shop),
    path('wishlist/', views.view_wishlist),
    path('wishlist/add/<prod_id>/', views.add_to_wishlist),
    path('wishlist/remove/<prod_id>/', views.remove_from_wishlist),
    path('product_details/<prod_id>/', views.product_details),
    path('cart/', views.view_cart),
    path('cart/add/<prod_id>/', views.add_to_cart),
    path('cart/add/<prod_id>/<quantity>/', views.add_to_cart),
    path('cart/update/<cart_id>/<quantity>/', views.update_cart),
    path('cart/remove/<prod_id>/', views.remove_from_cart),
    path('checkout/',views.checkout),
    path('checkout/placeorder/',views.placeorder),
    path('checkout/order_success/',views.order_success),
    path('order/view/<order_id>/',views.fetch_order)
]
