# Generated by Django 3.1.1 on 2020-11-06 18:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meetup_finder_app', '0003_customer'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Customer',
        ),
    ]