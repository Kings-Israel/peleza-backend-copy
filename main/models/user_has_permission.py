from django.db import models
from authentication.models import PelClient
from main.models.permissions import Permissions

class UserHasPermission(models.Model):
    permission = models.ForeignKey(Permissions, on_delete=models.CASCADE)
    user = models.ForeignKey(PelClient, on_delete=models.CASCADE)