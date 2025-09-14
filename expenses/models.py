from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
class Income(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    amount=models.IntegerField()
    date=models.DateTimeField()
    source=models.CharField(max_length=100)
    def clean(self):
        if self.amount < 0:
            raise ValueError("Income amount cannot be negative")
        if self.date> timezone.now():
            raise ValueError("Income date cannot be in the future")
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
    def __str__(self):
        return (f"income from {self.source}: {self.amount}.   Date: {self.date}")
class Outlay(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    amount=models.BigIntegerField()
    date=models.DateTimeField()
    category=models.CharField(max_length=100)
    def clean(self):
        if self.amount < 0:
            raise ValueError("Outlay amount cannot be negative")
        if self.date > timezone.now():
            raise ValueError("Outlay date cannot be in the future")
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
    def __str__(self):
        return (f"{self.category} cost:{self.amount}.   Date: {self.date}")

    

# Create your models here.
