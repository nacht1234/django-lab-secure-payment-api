from django.db import models

# Create your models here.
from django.db import models

class Payment(models.Model):
    name = models.CharField(max_length=100)
    encrypted_card = models.BinaryField()
    created_at = models.DateTimeField(auto_now_add=True)