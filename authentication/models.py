from django.db import models
import random, string, base64, hashlib, threading
from django.utils import timezone
from django.db.models import query
from hashlib import md5
from . import querry
# from main.models.user_has_permission import UserHasPermission


# Create your models here.
class ClientCompany(models.Model):
    company_id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=255, null=False, unique=True)
    company_email_address = models.CharField(max_length=255, null=False, unique=True)
    company_mobile_number = models.CharField(max_length=255, null=False, unique=True)
    status = models.CharField(max_length=255, null=False, default=22)
    added_date = models.CharField(max_length=255, null=True, blank=True)
    company_country = models.CharField(max_length=255, null=False)
    added_by = models.CharField(max_length=255, null=False)
    verified_by = models.CharField(max_length=255, null=True)
    company_industry = models.CharField(max_length=255, null=True)
    verified_date = models.CharField(max_length=255, null=True)
    company_logo = models.CharField(max_length=255, null=True)
    company_code = models.CharField(max_length=255, null=True, unique=True)
    company_credit = models.CharField(max_length=255, null=True)

    class Meta:
        managed = True
        db_table = "pel_client_co"


class PelClient(models.Model):
    client_id = models.AutoField(unique=True, editable=False, primary_key=True)
    client_company_id = models.CharField(max_length=200, blank=True, null=True, unique=False)
    client_login_username = models.CharField(
        max_length=200, blank=True, null=True, unique=True
    )
    client_password = models.CharField(max_length=255, blank=False, null=False)
    status = models.CharField(max_length=10, null=True, blank=True)
    # client_parent_company = models.CharField(max_length=255)
    client_parent_company = models.ForeignKey(
        "authentication.ClientCompany",
        models.CASCADE,
        related_name="company",
        db_column="client_parent_company",
        to_field="company_name",
    )
    
    client_pin = models.CharField(max_length=255)
   
    client_first_name = models.CharField(max_length=255)
    client_last_name = models.CharField(max_length=255)

    client_mobile_number = models.CharField(max_length=255, blank=True, null=True)
    client_postal_address = models.CharField(max_length=255, blank=True, null=True)
    client_postal_code = models.CharField(max_length=255, blank=True, null=True)
    client_city = models.CharField(max_length=255, blank=True, null=True)
    added_by = models.ForeignKey(
        "authentication.PelClient",
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    title = models.CharField(max_length=255, blank=True, null=True)
    
    REQUIRED_FIELDS = ("password", "company_name", "company_id")
    USERNAME_FIELD = "client_login_username"

    @property
    def email(self):
        return self.client_login_username

    @property
    def name(self):
        return ("%s %s" % (self.client_first_name, self.client_last_name)).title()

    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        return False

    @property
    def token(self):
        return self.client_pin

    class Meta:
        db_table = "pel_client"
        managed = True

    @classmethod
    def login(cls, client_id=None, username=None, password="", **kwargs):
        user = None
        password = hashlib.md5(password.encode()).hexdigest()

        try:
            user = cls.objects.get(
                client_login_username__iexact=username,
                client_password=password,
                client_company_id__iexact=client_id,
            )

        except:
            try:
                user = cls.objects.get(
                    client_login_username__iexact=username,
                    client_password=password,
                    client_parent_company__iexact=client_id,
                )
            except:
                pass

        finally:
            if user:
                token = cls.generate_token()
                user.client_pin = token
                thread = threading.Thread(target=user.save)
                thread.start()

            return user
    @classmethod
    def register(cls, first_name, last_name, email, mobile_number, password, city, company_id, company):
        print(company)
        user = None
        client_company = ClientCompany.objects.get(company_id=company_id[0])
        user = cls.objects.create(
            client_company_id=company[0],
            client_login_username=email[0],
            client_password=hashlib.md5(password[0].encode()).hexdigest(),
            client_first_name=first_name[0],
            client_last_name=last_name[0],
            client_mobile_number=mobile_number[0],
            client_postal_address='8817',
            client_postal_code='00100',
            client_city=city[0],
            client_parent_company=client_company,
        )

        if user:
                token = cls.generate_token()
                user.client_pin = token
                thread = threading.Thread(target=user.save)
                thread.start()

        return user
    
    @classmethod
    def generate_token(cls):
        strings = "%s%s%s" % (string.ascii_letters, string.digits, string.punctuation)
        raw_token = "".join(random.choices(strings, k=64))
        return base64.b64encode(raw_token.encode("ascii")).decode("ascii")
