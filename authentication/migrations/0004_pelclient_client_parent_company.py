# Generated by Django 4.2.3 on 2023-07-07 09:00

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_alter_clientcompany_options_alter_pelclient_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='pelclient',
            name='client_parent_company',
            field=models.ForeignKey(db_column='client_parent_company', default=django.utils.timezone.now, on_delete=django.db.models.deletion.CASCADE, related_name='company', to='authentication.clientcompany', to_field='company_name'),
            preserve_default=False,
        ),
    ]