# Generated by Django 3.0.8 on 2020-07-26 18:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_auto_20200725_1531'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productorderamount',
            name='buyer',
        ),
        migrations.AlterField(
            model_name='productorderamount',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.Product', unique=True),
        ),
    ]