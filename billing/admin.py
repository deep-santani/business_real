from django.contrib import admin

from .models import *
# Register your models here.
admin.site.register(Customer_detail)
admin.site.register(Sale)
admin.site.register(Payment)
admin.site.register(Item)