# Generated by Django 3.1.1 on 2020-11-11 22:09

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('meetup_finder_app', '0006_event_interested_users'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='interested_users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
