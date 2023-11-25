from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.html import format_html

# Register your models here.
from shop.models import Product, Cart, Wishlist, Order

class ReadOnlyAdminMixin:
    def has_change_permission(self, request, obj=None):
        return False  # Disable the ability to change (edit) records
    def has_add_permission(self, request):
        return False  # Disable the ability to add new records
    def has_delete_permission(self, request, obj=None):
        return False  # Disable the ability to add new records

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('display_image','product_name', 'product_category', 'price', 'status')
    list_editable = ('status',)

    def display_image(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" width="80" height="80" />')

    display_image.short_description = 'Image'



@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'order_date', 'total_amount', 'customer_details', 'display_product_details','order_status')
    list_editable = ('order_status',)

    def display_product_details(self, obj):
        products = obj.order_items.all()  # Update the related name
        product_details = '<br>'.join([f'{product.product_id.product_name}: {product.price}' for product in products])
        return mark_safe(product_details)

    display_product_details.short_description = 'Product Details'

    def customer_details(self, obj):
        return f'{obj.email_id.name}({obj.email_id.email_id})'

    customer_details.short_description = 'Customer Details'


@admin.register(Cart)
class CartAdmin(ReadOnlyAdminMixin,admin.ModelAdmin):
    list_display = ('id','product_image', 'product_name',  'user_name', 'user_email', 'quantity', 'subtotal')
    list_display_links = ()

    def product_name(self, obj):
        return obj.product_id.product_name

    def product_image(self, obj):
        if obj.product_id.image:
            return format_html('<img src="{}" alt="Product Image" width="50" height="50" />', obj.product_id.image.url)
        return '-'

    def user_name(self, obj):
        return obj.email_id.name if obj.email_id.name else ''

    def user_email(self, obj):
        return obj.email_id.email_id if obj.email_id.email_id else ''

    def subtotal(self, obj):
        return obj.calculate_subtotal()

@admin.register(Wishlist)
class WishlistAdmin(ReadOnlyAdminMixin,admin.ModelAdmin):
    list_display = ( 'product_image', 'product_name', 'user_name', 'user_email')
    list_display_links = ()

    def product_name(self, obj):
        return obj.product_id.product_name

    def product_image(self, obj):
        if obj.product_id.image:
            return format_html('<img src="{}" alt="Product Image" width="50" height="50" />', obj.product_id.image.url)
        return '-'

    def user_name(self, obj):
        return obj.email_id.name if obj.email_id.name else ''

    def user_email(self, obj):
        return obj.email_id.email_id if obj.email_id.email_id else ''