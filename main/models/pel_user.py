from django.db import models
from django.utils import timezone

class PelUser(models.Model):
    
    usr_id = models.IntegerField(primary_key=True)
    usr_mailer_id = models.IntegerField(null=True)
    usr_created_by = models.CharField(max_length=255, blank=True)
    usr_created_at = models.DateTimeField(null=True)
    usr_date_modified = models.DateTimeField(null=True)
    usr_last_password_change = models.CharField(max_length=255, blank=True)
    usr_modified_by = models.CharField(max_length=255, blank=True)
    usr_name = models.CharField(max_length=255, blank=True)
    usr_password = models.CharField(max_length=255, blank=True)
    usr_phone_number = models.CharField(max_length=20, blank=True)
    usr_retries = models.CharField(max_length=255, blank=True, null=True)
    usr_staff_id = models.CharField(max_length=255, blank=True, null=True)
    usr_status = models.CharField(max_length=255, blank=True, null=True)
    usr_username = models.CharField(max_length=255, blank=True, null=True)
    fk_institution_id = models.CharField(max_length=255, blank=True, null=True)
    usr_pin = models.CharField(max_length=50)
    usr_pin_status = models.CharField(max_length=10)
    usr_photo = models.CharField(max_length=255)
    usr_last_login = models.DateField(default=timezone.now, null=True)
    usr_national_id = models.CharField(max_length=255, blank=True)
    usr_profile_id = models.CharField(max_length=255, blank=True)
    usr_profile_name = models.CharField(max_length=50, null=True)
    usr_email = models.EmailField(max_length=255, blank=True)

    class Meta:
        db_table = "pel_users"
        managed = True
