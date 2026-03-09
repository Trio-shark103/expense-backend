from django.contrib import admin
from .models import Category, Transaction, Department, UserDetail



class TransactionAdmin(admin.ModelAdmin):
    prepopulated_fields={'narration': ('narration', )}
    list_display = ('category', 'author','department', 'transaction_type', 'amount', 'is_deleted')
    search_fields = ('id', 'category__category_name', 'transaction_type')
    list_filter = ('category', 'date', 'author', 'transaction_type')
    list_editable = ('is_deleted',)



# Register your models here.
admin.site.register(Category)
admin.site.register(Department)
admin.site.register(UserDetail)
admin.site.register(Transaction, TransactionAdmin)
