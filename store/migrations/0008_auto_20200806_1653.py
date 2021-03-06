# Generated by Django 3.0.8 on 2020-08-06 13:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_auto_20200731_1859'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductOrderDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=1)),
                ('total_price', models.PositiveIntegerField(default=0)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.Order')),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='store.Product')),
            ],
        ),
        migrations.DeleteModel(
            name='ProductOrderAmount',
        ),
    ]
