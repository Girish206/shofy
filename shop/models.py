from django.utils import timezone
from django.db import models
from main.models import Users, ShippingAddress


STATUS_CHOICES = [
    ('In Stock', 'In Stock'),
    ('Out Of Stock', 'Out Of Stock'),
]

ORDER_STATUS_CHOICES = [
    ('Order Confirmed', 'Order Confirmed'),
    ('Shipped', 'Shipped'),
    ('Out For Delivery', 'Out For Delivery'),
    ('Delivered', 'Delivered'),
]

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    product_type = models.CharField(max_length=200)
    product_category = models.CharField(max_length=200)
    product_name = models.CharField(max_length=200)
    product_brand = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField()
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='In Stock')
    discount = models.DecimalField(max_digits=8, decimal_places=1, default=0)
    image = models.ImageField(upload_to='images/')

    def discount_price(self):
        return round((self.price - (self.discount / 100) * self.price),2)


class Cart(models.Model):
    id = models.AutoField(primary_key=True)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    email_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True)

    def calculate_subtotal(self):
        return round((self.product_id.discount_price()) * (self.quantity), 2)


class Wishlist(models.Model):
    id = models.AutoField(primary_key=True)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    email_id = models.ForeignKey(Users, on_delete=models.CASCADE)


class Order(models.Model):
    order_id = models.CharField(max_length=255,primary_key=True)
    email_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    order_date = models.DateTimeField(default=timezone.now)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.CASCADE)
    order_status=models.CharField(max_length=100,choices=ORDER_STATUS_CHOICES, default='Order Confirmed')
    products = models.ManyToManyField(Product, through='Order_items')

    def formatted_order_date(self):
        return self.order_date.strftime('%d %b %Y')

class Order_items(models.Model):
    id = models.AutoField(primary_key=True)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    price=models.DecimalField(max_digits=8,decimal_places=2,null=True)
    quantity = models.IntegerField(null=True)
