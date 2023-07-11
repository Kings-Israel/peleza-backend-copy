# Generated by Django 4.2.3 on 2023-07-10 11:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_pelclient_client_parent_company'),
    ]

    operations = [
        migrations.AddField(
            model_name='pelclient',
            name='added_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
