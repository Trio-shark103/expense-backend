from django.contrib import admin
from .models import Category, Transaction



class TransactionAdmin(admin.ModelAdmin):
    prepopulated_fields={'title': ('title', )}
    list_display = ('title', 'category', 'author', 'transaction_type', 'amount')
    search_fields = ('id', 'title', 'category__category_name', 'status')



# Register your models here.
admin.site.register(Category)

admin.site.register(Transaction, TransactionAdmin)
