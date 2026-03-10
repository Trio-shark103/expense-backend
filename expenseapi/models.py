from django.db import models
from django.contrib.auth.models import User


TRANSACTION_CHOICES = (
    ("Income", "Income"),
    ("Expense", "Expense")
)

# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        verbose_name_plural = 'categories'
    
    def __str__(self):
        return self.category_name
    

class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Transaction(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_CHOICES, default="Expense")
    department = models.ForeignKey(Department, on_delete=models.CASCADE ,null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    narration = models.TextField(max_length=500, blank=True)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return f"{self.category}"
    

class UserDetail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="userdetail", null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.user.username