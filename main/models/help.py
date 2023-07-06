from django.db import models

class FormData(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    subject = models.CharField(max_length=200)
    image = models.CharField(max_length=200)# Add ImageField
    message = models.TextField() 
    # Add more fields as per your form data structure

    def __str__(self):
        return f"{self.first_name} {self.last_name}"