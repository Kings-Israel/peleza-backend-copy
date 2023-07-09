from django.db import models
from authentication.models import PelClient

class AddUser(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    city = models.CharField(max_length=200)
    address = models.CharField(max_length=200)# Add ImageField
    added_by = models.ForeignKey(PelClient, on_delete=models.CASCADE)
    company = models.ForeignKey(
        PelClient,
        on_delete=models.CASCADE,
        to_field='client_company_id',
        db_column='company',
        related_name='user_set',
        null=True,
    )
    role = models.CharField(max_length=200, default='user')
    # Add more fields as per your form data structure

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
