# Generated by Django 3.0.8 on 2020-09-17 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0018_auto_20200914_2213'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_method',
            field=models.CharField(choices=[('On receipt', 'On Receipt'), ('Bank Transaction', 'Bank Transaction'), ('Qiwi wallet', 'Qiwi Wallet')], default='On receipt', max_length=30),
        ),
        migrations.AddField(
            model_name='order',
            name='shipping_method',
            field=models.CharField(choices=[('Pickup', 'Pickup'), ('City courier delivery', 'City Courier Delivery'), ('Boxberry', 'Boxberry')], default='Pickup', max_length=30),
        ),
    ]
