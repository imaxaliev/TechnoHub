# Generated by Django 3.0.8 on 2020-07-26 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_auto_20200726_2158'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productorderamount',
            old_name='ordered_amount',
            new_name='amount',
        ),
        migrations.AddField(
            model_name='laptopparam',
            name='thickness',
            field=models.DecimalField(decimal_places=1, default=None, help_text='sm', max_digits=2),
        ),
    ]
