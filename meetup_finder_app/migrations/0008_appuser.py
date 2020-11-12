# Generated by Django 3.1.1 on 2020-11-12 06:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('meetup_finder_app', '0007_auto_20201111_2209'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppUser',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('django_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('friends', models.ManyToManyField(related_name='_appuser_friends_+', to='meetup_finder_app.AppUser')),
            ],
        ),
    ]