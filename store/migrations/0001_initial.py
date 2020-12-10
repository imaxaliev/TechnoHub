# Generated by Django 3.0.8 on 2020-07-25 11:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=40)),
                ('slug', models.SlugField(default=None, null=True)),
                ('parent_cat', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.Category')),
            ],
            options={
                'verbose_name_plural': 'categories',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Manufacturer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('specialization', models.ManyToManyField(to='store.Category')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_method', models.CharField(choices=[('On receipt', 'On Receipt'), ('Bank transaction', 'Bank Transaction'), ('Emoney', 'Emoney')], default='On receipt', max_length=30)),
                ('shipping_method', models.CharField(choices=[('Pickup', 'Pickup'), ('City courier delivery', 'City Courier Delivery'), ("Russia's post", 'Russia Post'), ('Cdek', 'Cdek')], default='Pickup', max_length=30)),
                ('status', models.CharField(choices=[('In process', 'In Process'), ('On the way', 'On The Way'), ('Await', 'Await'), ('Completed', 'Completed'), ('Declined', 'Declined')], default='In process', max_length=30)),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('slug', models.SlugField(default=None, null=True)),
                ('model_series', models.CharField(max_length=30)),
                ('description', models.TextField(default=None, null=True)),
                ('price', models.PositiveIntegerField(default=0)),
                ('in_stock_amount', models.PositiveIntegerField(default=0)),
                ('warehouse_amount', models.PositiveIntegerField(default=0)),
                ('times_purchased', models.PositiveIntegerField(default=0)),
                ('lbl_is_popular', models.BooleanField(default=False, verbose_name='Is popular')),
                ('sale_percent', models.PositiveIntegerField(default=0)),
                ('sale_value', models.PositiveIntegerField(default=0)),
                ('total_price', models.PositiveIntegerField(default=0)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.Category')),
                ('manufacturer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.Manufacturer')),
            ],
        ),
        migrations.CreateModel(
            name='ProductOrderAmount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordered_amount', models.IntegerField(default=1)),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.Order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.Product')),
            ],
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', sorl.thumbnail.fields.ImageField(upload_to='products/')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.Product')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='product',
            field=models.ManyToManyField(to='store.Product'),
        ),
        migrations.CreateModel(
            name='LaptopParam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('processor', models.CharField(max_length=30)),
                ('physical_memory', models.CharField(max_length=30)),
                ('ram', models.CharField(max_length=30)),
                ('screen_size', models.DecimalField(decimal_places=1, max_digits=3)),
                ('screen_resolution', models.CharField(max_length=20)),
                ('cache_memory', models.CharField(max_length=30)),
                ('corpus', models.CharField(max_length=50)),
                ('autonomous_work_time', models.TimeField()),
                ('dynamics', models.CharField(max_length=20)),
                ('mic', models.CharField(max_length=20)),
                ('graphics_card', models.CharField(max_length=40)),
                ('os', models.CharField(max_length=20)),
                ('additional_utils', models.CharField(max_length=100)),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='store.Product')),
            ],
        ),
    ]