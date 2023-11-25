from django.contrib import admin
from django.utils.html import format_html

from .models import Users, ShippingAddress, ContactUs

@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('display_photo','email_id', 'name', 'mobile_number')
    list_display_links = ('email_id', 'name')

    def display_photo(self, obj):
        if obj.photo:
            return format_html('<img src="{}" alt="User Photo" width="50" height="50" />', obj.photo.url)
        return '-'

    display_photo.short_description = 'User Photo'


@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'email_id', 'name', 'mobile_number', 'house_no', 'area', 'landmark', 'pincode', 'city', 'state', 'default_address')
    list_display_links = ('id', 'email_id')

@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email_id', 'mobile_number', 'message')
    list_display_links = ('id', 'first_name', 'last_name')
