# Generated by Django 3.2.3 on 2021-12-05 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PelClient',
            fields=[
                ('client_id', models.AutoField(editable=False, primary_key=True, serialize=False, unique=True)),
                ('client_company_id', models.CharField(blank=True, max_length=200, null=True, unique=False)),
                ('client_login_username', models.CharField(blank=True, max_length=200, null=True, unique=True)),
                ('client_password', models.CharField(max_length=255)),
                ('status', models.CharField(blank=True, max_length=10, null=True)),
                ('client_pin', models.CharField(max_length=255)),
                ('client_first_name', models.CharField(max_length=255)),
                ('client_last_name', models.CharField(max_length=255)),
                ('client_mobile_number', models.CharField(blank=True, max_length=255, null=True)),
                ('client_postal_address', models.CharField(blank=True, max_length=255, null=True)),
                ('client_postal_code', models.CharField(blank=True, max_length=255, null=True)),
                ('client_city', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'pel_client',
                # "managed": False,
            },
        ),
        migrations.CreateModel(
            name='ClientCompany',
            fields=[
                ('company_id', models.AutoField(primary_key=True, serialize=False)),
                ('company_name', models.CharField(max_length=255, unique=True)),
                ('company_email_address', models.CharField(max_length=255, unique=True)),
                ('company_mobile_number', models.CharField(max_length=255, unique=True)),
                ('status', models.CharField(default=22, max_length=255)),
                ('added_date', models.CharField(blank=True, max_length=255, null=True)),
                ('company_country', models.CharField(max_length=255)),
                ('added_by', models.CharField(max_length=255)),
                ('verified_by', models.CharField(max_length=255, null=True)),
                ('company_industry', models.CharField(max_length=255, null=True)),
                ('verified_date', models.CharField(max_length=255, null=True)),
                ('company_logo', models.CharField(max_length=255, null=True)),
                ('company_code', models.CharField(max_length=255, null=True, unique=True)),
                ('company_credit', models.CharField(max_length=255, null=True)),
            ],
            options={
                'db_table': 'pel_client_co',
                # "managed": False,
            },
        ),
    ]
