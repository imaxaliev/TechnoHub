# Generated by Django 3.0.8 on 2020-07-31 15:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_auto_20200727_2311'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productimage',
            old_name='main',
            new_name='is_default',
        ),
    ]
