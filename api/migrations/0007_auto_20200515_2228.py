# Generated by Django 3.0.4 on 2020-05-15 22:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20200515_2143'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feeditemcomment',
            name='feedItem',
        ),
        migrations.AddField(
            model_name='feeditemcomment',
            name='feed_item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.FeedItem'),
        ),
    ]
