from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.utils import timezone
class Income(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    amount=models.IntegerField()
    date=models.DateTimeField()
    source=models.CharField(max_length=100)
    def clean(self):
        if self.amount < 0:
            raise ValidationError("Income amount cannot be negative")
        if self.date > timezone.now():
            raise ValidationError("Income date cannot be in the future")
    def save(self):
        self.clean()
        super().save()
    def __str__(self):
        return (f"income from {self.source}: {self.amount}.   Date: {self.date}")
class Expense(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    amount=models.BigIntegerField()
    date=models.DateTimeField()
    text=models.CharField(max_length=100)
    def clean(self):
        if self.amount < 0:
            raise ValidationError("Expense amount cannot be negative")
        if self.date > timezone.now():
            raise ValidationError("Expense date cannot be in the future")
    def save(self):
        self.clean()
        super().save()
    def __str__(self):
        return (f"{self.text} cost:{self.amount}.   Date: {self.date}")

    

# Create your models here.
