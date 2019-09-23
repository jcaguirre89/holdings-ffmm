from django.db import models

class Holding(models.Model):
    run = models.CharField(max_length=15)
    quantity = models.PositiveIntegerField()
