from django.db import models

# Create your models here.
from django.db import models

class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    nfc_uid = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name