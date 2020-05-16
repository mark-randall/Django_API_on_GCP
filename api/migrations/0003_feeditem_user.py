# Generated by Django 3.0.4 on 2020-05-16 22:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20200516_2126'),
    ]

    operations = [
        migrations.AddField(
            model_name='feeditem',
            name='user',
            field=models.ForeignKey(blank=True, default='1', on_delete=django.db.models.deletion.CASCADE, related_name='feed', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
