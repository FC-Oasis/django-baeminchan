# Generated by Django 2.1 on 2018-08-22 09:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_auto_20180822_0832'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='thumbnail_url',
            new_name='thumbnail_url1',
        ),
    ]
