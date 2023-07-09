# Generated by Django 4.2.3 on 2023-07-09 11:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0005_adduser'),
    ]

    operations = [
        migrations.AddField(
            model_name='adduser',
            name='company',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='employees', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='adduser',
            name='role',
            field=models.CharField(default='user', max_length=200),
        ),
        migrations.AlterField(
            model_name='adduser',
            name='added_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
