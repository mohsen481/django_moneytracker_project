from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
class Income(models.Model):
    user=models.ForeignKey("auth.User",related_name="incomes",on_delete=models.CASCADE,null=True)
    amount=models.IntegerField()
    date=models.DateTimeField()
    source=models.CharField(max_length=100)
    def clean(self):
        if self.amount < 0:
            raise ValidationError("Income amount cannot be negative")
        if self.date > timezone.now():
            raise ValidationError("Income date cannot be in the future")
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
    def __str__(self):
        return (f"income from {self.source}: {self.amount}.   Date: {self.date}")
class Expense(models.Model):
    user=models.ForeignKey("auth.User",related_name="expenses",on_delete=models.CASCADE,null=True)
    amount=models.BigIntegerField()
    date=models.DateTimeField()
    text=models.CharField(max_length=100)
    def clean(self):
        if self.amount < 0:
            raise ValidationError("Expense amount cannot be negative")
        if self.date > timezone.now():
            raise ValidationError("Expense date cannot be in the future")
    def save(self,*args,**kwargs):
        self.clean()
        super().save(*args,**kwargs)
    def __str__(self):
        return (f"{self.text} cost:{self.amount}.   Date: {self.date}")

    

# Create your models here.
