from django.db import models
from django.contrib.auth.models import User


TRANSACTION_CHOICES = (
    ("Income", "Income"),
    ("Expense", "Expense")
)

# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    status = models.CharField(choices=TRANSACTION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        verbose_name_plural = 'categories'
    
    def __str__(self):
        return self.category_name


class Income(models.Model):
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.total_amount}"



class Expense(models.Model):
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.total_amount}"
    
    

class Transaction(models.Model):
    title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=TRANSACTION_CHOICES, default="Expense")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(max_length=500, blank=True)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return self.title