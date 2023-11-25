# Generated by Django 4.2.1 on 2023-09-09 22:36

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order_id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('order_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('email_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.users')),
                ('shipping_address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.shippingaddress')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('product_type', models.CharField(max_length=200)),
                ('product_category', models.CharField(max_length=200)),
                ('product_name', models.CharField(max_length=200)),
                ('product_brand', models.CharField(max_length=200)),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('description', models.TextField()),
                ('status', models.CharField(default='In Stock', max_length=20)),
                ('discount', models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                ('image', models.ImageField(upload_to='images/')),
            ],
        ),
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('email_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.users')),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.product')),
            ],
        ),
        migrations.CreateModel(
            name='Order_items',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('price', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('quantity', models.IntegerField(null=True)),
                ('order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.order')),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.product')),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('quantity', models.IntegerField(null=True)),
                ('email_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.users')),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.product')),
            ],
        ),
    ]
