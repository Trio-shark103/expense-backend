from django.contrib import admin
from .models import Category, Income, Expense, Transaction


class TransactionAdmin(admin.ModelAdmin):
    prepopulated_fields={'title': ('title', )}
    list_display = ('title', 'category', 'author', 'status', 'amount')
    search_fields = ('id', 'title', 'category__category_name', 'status')


# Register your models here.
admin.site.register(Category)
admin.site.register(Income)
admin.site.register(Expense)
admin.site.register(Transaction, TransactionAdmin)
