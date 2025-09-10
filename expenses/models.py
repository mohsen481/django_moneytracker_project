from django.db import models
class Income(models.Model):
    amount=models.IntegerField()
    date=models.DateTimeField(auto_now=True)
    source=models.CharField(max_length=100)
    def __str__(self):
        return (f"income from {self.source}: {self.amount}.   Date: {self.date}")
class Outlay(models.Model):
    amount=models.BigIntegerField()
    date=models.DateTimeField(auto_now=True)
    category=models.CharField(max_length=100)
    def __str__(self):
        return (f"{self.category} cost: {self.amount}.   Date: {self.date}")

    

# Create your models here.
