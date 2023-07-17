# Generated by Django 3.2.3 on 2023-07-13 14:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PelPsmtRequestModules',
            fields=[
                ('request_package_id', models.AutoField(primary_key=True, serialize=False)),
                ('request_ref_number', models.CharField(blank=True, max_length=255, null=True)),
                ('status', models.CharField(blank=True, max_length=255, null=True)),
                ('client_id', models.CharField(blank=True, max_length=255, null=True)),
                ('package_id', models.CharField(blank=True, max_length=255, null=True)),
                ('package_name', models.CharField(blank=True, max_length=255, null=True)),
                ('module_name', models.CharField(blank=True, max_length=255, null=True)),
                ('request_type', models.CharField(blank=True, max_length=255, null=True)),
                ('request_id', models.CharField(blank=True, max_length=255, null=True)),
                ('module_id', models.CharField(blank=True, max_length=255, null=True)),
                ('parent_module_id', models.CharField(blank=True, max_length=255, null=True)),
                ('module_cost_quote', models.CharField(blank=True, max_length=255, null=True)),
                ('by_pass', models.DecimalField(blank=True, decimal_places=0, max_digits=11, null=True)),
                ('valid', models.DecimalField(blank=True, decimal_places=0, max_digits=11, null=True)),
            ],
            options={
                'db_table': 'pel_psmt_request_modules',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='BgRequestModule',
            fields=[
                ('request_package_id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.CharField(default='00', max_length=255, null=True)),
                ('client_id', models.CharField(max_length=255, null=True)),
                ('package_id', models.CharField(max_length=255, null=True)),
                ('package_name', models.CharField(max_length=255, null=True)),
                ('module_name', models.CharField(max_length=255, null=True)),
                ('request_type', models.CharField(max_length=255, null=True)),
                ('request_id', models.CharField(max_length=255, null=True)),
                ('module_id', models.CharField(max_length=255, null=True)),
                ('parent_module_id', models.CharField(max_length=255, null=True)),
                ('module_cost_quote', models.CharField(max_length=255, null=True)),
            ],
            options={
                'db_table': 'pel_psmt_request_modules',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='BusinessCompanyReg',
            fields=[
                ('company_reg_id', models.AutoField(editable=False, primary_key=True, serialize=False, unique=True)),
                ('business_name', models.CharField(db_column='company_name', max_length=255)),
                ('status', models.CharField(default='11', max_length=255)),
                ('kra_pin', models.CharField(blank=True, max_length=255, null=True)),
                ('registration_number', models.CharField(max_length=255, null=True, unique=True)),
                ('registration_date', models.CharField(max_length=255, null=True)),
                ('objective', models.CharField(blank=True, default='-', help_text='Added specifically for NGO and Society', max_length=255, null=True)),
                ('member_count', models.CharField(blank=True, default='-', help_text='Added specifically for NGO', max_length=255, null=True)),
                ('physical_address', models.CharField(db_column='address', max_length=255)),
                ('postal_address', models.CharField(max_length=255, null=True)),
                ('branches', models.TextField(blank=True, db_column='offices', null=True)),
                ('email', models.CharField(blank=True, db_column='email_address', max_length=355, null=True)),
                ('phone_number', models.CharField(db_column='mobile_number', max_length=255)),
                ('verified', models.BooleanField(null=True)),
                ('type', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'pel_company_registration',
                'ordering': ['-pk'],
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Encumbrance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('search_id', models.CharField(blank=True, max_length=255, null=True)),
                ('status', models.CharField(default='11', max_length=255)),
                ('description_of_evidence', models.TextField(blank=True, db_column='description', max_length=255, null=True)),
                ('date_of_evidence', models.CharField(blank=True, db_column='date', max_length=255, null=True)),
                ('verified_by', models.CharField(blank=True, max_length=255, null=True)),
                ('review_notes', models.TextField(blank=True, null=True)),
                ('review_status', models.CharField(blank=True, help_text='APPROVED or REJECTED', max_length=255, null=True)),
                ('verified_date', models.DateTimeField()),
                ('secured_amounts', models.CharField(blank=True, db_column='amount_secured', max_length=255, null=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateField(auto_now=True)),
                ('business', models.ForeignKey(db_column='business', on_delete=django.db.models.deletion.CASCADE, related_name='encumbrances', to='main.businesscompanyreg')),
            ],
            options={
                'db_table': 'pel_company_encumbrances',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('module_id', models.AutoField(primary_key=True, serialize=False)),
                ('module_name', models.CharField(max_length=255, null=True, unique=True)),
                ('status', models.CharField(default='11', max_length=255, null=True)),
                ('module_date_added', models.DateField(auto_now_add=True)),
                ('module_added_by', models.CharField(max_length=255, null=True)),
                ('module_verified_by', models.CharField(max_length=255, null=True)),
                ('module_code', models.CharField(max_length=255, null=True)),
                ('module_parent', models.CharField(max_length=255, null=True)),
                ('module_cost', models.CharField(max_length=255, null=True)),
                ('cost_review', models.CharField(max_length=255, null=True)),
                ('module_role', models.CharField(max_length=255, null=True)),
                ('module_cost_currency', models.CharField(max_length=255, null=True)),
                ('module_credits', models.CharField(max_length=255, null=True)),
            ],
            options={
                'db_table': 'pel_module',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Package',
            fields=[
                ('package_id', models.AutoField(primary_key=True, serialize=False)),
                ('package_name', models.CharField(max_length=255)),
                ('package_cost', models.CharField(max_length=255, null=True)),
                ('package_status', models.CharField(default='22', max_length=255)),
                ('package_added_by', models.CharField(max_length=255, null=True)),
                ('package_added_date', models.CharField(max_length=255, null=True)),
                ('package_data', models.CharField(max_length=255, null=True)),
                ('package_verified_by', models.CharField(max_length=255, null=True)),
                ('package_verified_date', models.CharField(max_length=255, null=True)),
                ('dataset_id', models.CharField(max_length=255, null=True)),
                ('package_currency', models.CharField(max_length=255, null=True)),
                ('package_min', models.CharField(max_length=255, null=True)),
                ('package_max', models.CharField(max_length=255, null=True)),
                ('package_credits', models.CharField(max_length=255, null=True)),
                ('package_general', models.CharField(default=0, max_length=255, null=True)),
                ('package_cost_discount', models.CharField(max_length=255, null=True)),
                ('package_credits_discount', models.CharField(max_length=255, null=True)),
                ('package_data_type', models.CharField(max_length=255, null=True)),
            ],
            options={
                'db_table': 'pel_package',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='PackageModule',
            fields=[
                ('modulepackage_id', models.AutoField(primary_key=True, serialize=False)),
                ('module_name', models.CharField(max_length=255)),
                ('status', models.CharField(default='00', max_length=255)),
                ('added_by', models.CharField(max_length=255, null=True)),
                ('added_date', models.DateField(auto_now_add=True)),
                ('verified_by', models.CharField(max_length=255, null=True)),
                ('verified_date', models.CharField(max_length=255, null=True)),
                ('package_id', models.CharField(max_length=255, null=True)),
                ('package_name', models.CharField(max_length=255, null=True)),
                ('module_id', models.CharField(max_length=255, null=True)),
                ('module_cost', models.CharField(max_length=255, null=True)),
                ('cost_currency', models.CharField(max_length=255, null=True)),
                ('cost_review', models.CharField(max_length=255, null=True)),
                ('package_data_type', models.CharField(max_length=255, null=True)),
            ],
            options={
                'db_table': 'pel_packages_module',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='PelUser',
            fields=[
                ('usr_id', models.IntegerField(primary_key=True, serialize=False)),
                ('usr_mailer_id', models.IntegerField(null=True)),
                ('usr_created_by', models.CharField(blank=True, max_length=255)),
                ('usr_created_at', models.DateTimeField(null=True)),
                ('usr_date_modified', models.DateTimeField(null=True)),
                ('usr_last_password_change', models.CharField(blank=True, max_length=255)),
                ('usr_modified_by', models.CharField(blank=True, max_length=255)),
                ('usr_name', models.CharField(blank=True, max_length=255)),
                ('usr_password', models.CharField(blank=True, max_length=255)),
                ('usr_phone_number', models.CharField(blank=True, max_length=20)),
                ('usr_retries', models.CharField(blank=True, max_length=255, null=True)),
                ('usr_staff_id', models.CharField(blank=True, max_length=255, null=True)),
                ('usr_status', models.CharField(blank=True, max_length=255, null=True)),
                ('usr_username', models.CharField(blank=True, max_length=255, null=True)),
                ('fk_institution_id', models.CharField(blank=True, max_length=255, null=True)),
                ('usr_pin', models.CharField(max_length=50)),
                ('usr_pin_status', models.CharField(max_length=10)),
                ('usr_photo', models.CharField(max_length=255)),
                ('usr_last_login', models.DateField(default=django.utils.timezone.now, null=True)),
                ('usr_national_id', models.CharField(blank=True, max_length=255)),
                ('usr_profile_id', models.CharField(blank=True, max_length=255)),
                ('usr_profile_name', models.CharField(max_length=50, null=True)),
            ],
            options={
                'db_table': 'pel_users',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Permissions',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False, unique=True)),
                ('permission', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='UserHasPermission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('permission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.permissions')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Shares',
            fields=[
                ('shares_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('first_name', models.CharField(max_length=255, null=True)),
                ('second_name', models.CharField(max_length=255, null=True)),
                ('third_name', models.CharField(max_length=255, null=True)),
                ('status', models.CharField(default='11', max_length=255)),
                ('share_type', models.CharField(blank=True, help_text='name from external data, share_type in the db', max_length=255, null=True)),
                ('id_type', models.CharField(blank=True, max_length=255, null=True)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('nationality', models.CharField(blank=True, db_column='citizenship', max_length=255, null=True)),
                ('id_number', models.CharField(blank=True, max_length=255, null=True)),
                ('number_of_shares', models.CharField(blank=True, db_column='shares_number', max_length=255, null=True)),
                ('percentage', models.CharField(blank=True, max_length=255, null=True)),
                ('data_source', models.CharField(blank=True, max_length=255, null=True)),
                ('review_notes', models.TextField(blank=True, null=True)),
                ('review_status', models.CharField(blank=True, help_text='APPROVED or REJECTED', max_length=255, null=True)),
                ('added_by', models.CharField(blank=True, max_length=255, null=True)),
                ('verified_by', models.CharField(blank=True, max_length=255, null=True)),
                ('business', models.ForeignKey(blank=True, db_column='business', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='partners', to='main.businesscompanyreg')),
            ],
            options={
                'db_table': 'pel_company_shares_data',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='ShareCapital',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_of_shares', models.CharField(max_length=255, null=True)),
                ('nominal_value', models.CharField(blank=True, max_length=255, null=True)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('business', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='share_capital', to='main.businesscompanyreg')),
            ],
            options={
                'db_table': 'pel_company_share_capital',
            },
        ),
        migrations.CreateModel(
            name='PSMTRequest',
            fields=[
                ('request_id', models.AutoField(primary_key=True, serialize=False)),
                ('client_number', models.CharField(blank=True, max_length=200, null=True)),
                ('company_name', models.CharField(max_length=255, null=True)),
                ('registration_number', models.CharField(blank=True, max_length=200, null=True)),
                ('dataset_citizenship', models.CharField(max_length=255, null=True)),
                ('company_type', models.CharField(max_length=255, null=True)),
                ('request_plan', models.CharField(max_length=255, null=True)),
                ('bg_dataset_name', models.CharField(max_length=255, null=True)),
                ('request_ref_number', models.CharField(default=uuid.uuid4, max_length=255, unique=True)),
                ('status', models.CharField(default='33', max_length=255, null=True)),
                ('request_payment_ref', models.CharField(max_length=255, null=True)),
                ('client_id', models.CharField(max_length=255, null=True)),
                ('request_date', models.DateTimeField(auto_now_add=True)),
                ('request_terms', models.CharField(max_length=255, null=True)),
                ('package_cost', models.CharField(max_length=255, null=True)),
                ('request_dataset_cat', models.CharField(max_length=255, null=True)),
                ('client_name', models.CharField(max_length=255, null=True)),
                ('dataset_kra_pin', models.CharField(max_length=255, null=True)),
                ('dataset_incorporation_no', models.CharField(max_length=255, null=True)),
                ('bg_dataset_email', models.CharField(max_length=255, null=True)),
                ('bg_dataset_mobile', models.CharField(max_length=255, null=True)),
                ('bg_dataset_idnumber', models.CharField(max_length=20, null=True)),
                ('user_id', models.CharField(max_length=255, null=True)),
                ('user_name', models.CharField(max_length=255, null=True)),
                ('user_lock', models.CharField(max_length=255, null=True)),
                ('notify_by', models.CharField(max_length=255, null=True)),
                ('notify_date', models.DateTimeField(null=True)),
                ('user_lock_date', models.DateTimeField(max_length=255, null=True)),
                ('file_tracker', models.CharField(max_length=255, null=True)),
                ('comments', models.CharField(max_length=255, null=True)),
                ('request_package', models.CharField(max_length=255, null=True)),
                ('dataset_name', models.CharField(max_length=255, null=True)),
                ('report_file', models.CharField(max_length=255, null=True)),
                ('parent_name', models.CharField(max_length=255, null=True)),
                ('request_type', models.CharField(choices=[('individual', 'INDIVIDUAL'), ('company', 'COMPANY')], max_length=255, null=True)),
                ('dataset_photo', models.CharField(max_length=255, null=True)),
                ('client_login_id', models.CharField(max_length=255, null=True)),
                ('progress_calculator', models.CharField(max_length=255, null=True)),
                ('verified_date', models.DateTimeField(max_length=255, null=True)),
                ('quotation_by', models.CharField(max_length=255, null=True)),
                ('quotation_date', models.DateTimeField(null=True)),
                ('assigned_by', models.CharField(max_length=255, null=True)),
                ('assigned_date', models.DateTimeField(null=True)),
                ('status_date', models.DateTimeField(auto_now=True)),
                ('request_quotation_ref', models.CharField(max_length=255, null=True)),
                ('request_credit_charged', models.CharField(max_length=255, null=True)),
                ('package_cost_currency', models.CharField(max_length=255, null=True)),
                ('verification_status', models.CharField(default='00', max_length=255, null=True)),
                ('verified_by', models.CharField(max_length=255, null=True)),
                ('adverse_status', models.CharField(max_length=255, null=True)),
                ('final_notify', models.BooleanField(default=False)),
                ('negative', models.BooleanField(db_column='callback_url', default=False, max_length=200)),
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.package')),
            ],
            options={
                'db_table': 'pel_psmt_request',
                'ordering': ['-pk', 'bg_dataset_name'],
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='FormData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(max_length=20)),
                ('subject', models.CharField(max_length=200)),
                ('image', models.CharField(max_length=200)),
                ('message', models.TextField()),
                ('response', models.TextField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EncumbrancePersonsEntitled',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateField(auto_now=True)),
                ('encumbrance', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='persons_entitled', to='main.encumbrance')),
            ],
            options={
                'db_table': 'pel_company_persons_entitled',
            },
        ),
        migrations.CreateModel(
            name='CompanyOfficialDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(blank=True, max_length=255, null=True)),
                ('name', models.CharField(max_length=255, null=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateField(auto_now=True)),
                ('business', models.ForeignKey(db_column='company_id', on_delete=django.db.models.deletion.CASCADE, related_name='officials', to='main.businesscompanyreg')),
            ],
            options={
                'db_table': 'pel_company_official_details',
            },
        ),
        migrations.AddField(
            model_name='businesscompanyreg',
            name='request_ref_number',
            field=models.OneToOneField(blank=True, db_column='search_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='business', to='main.psmtrequest', to_field='request_ref_number'),
        ),
    ]
