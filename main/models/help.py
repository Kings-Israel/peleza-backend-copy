from django.db import models
from authentication.models import PelClient

class FormData(models.Model):
    user = models.ForeignKey(PelClient, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    subject = models.CharField(max_length=200)
    image = models.CharField(max_length=200)# Add ImageField
    message = models.TextField()
    response = models.TextField(null=True, blank=True)
    # Add more fields as per your form data structure

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class HelpSubject(models.Model):
    user = models.ForeignKey(PelClient, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

class HelpMessage(models.Model):
    subject = models.ForeignKey(HelpSubject, on_delete=models.CASCADE, related_name='messages')
    message = models.TextField(max_length=1000)
    read_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class HelpResponse(models.Model):
    subject = models.ForeignKey(HelpSubject, on_delete=models.CASCADE, related_name='responses')
    response = models.TextField(max_length=1000)
    read_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)