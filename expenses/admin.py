from django.contrib import admin
from .models import Expense,Category
# Register your models here.
#user1 123456 -superuser
admin.site.register(Expense)
admin.site.register(Category)