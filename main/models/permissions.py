from django.db import models

class Permissions(models.Model):
  
    id = models.AutoField(unique=True, editable=False, primary_key=True)
    permission = models.CharField(max_length=200)

    
