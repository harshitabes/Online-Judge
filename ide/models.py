from django.db import models

class Problem(models.Model):
    statement = models.CharField(max_length=1000)

# Create your models here.
