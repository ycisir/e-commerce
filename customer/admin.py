from django.contrib import admin
from customer.models import Customer


@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'customer_name', 'locality', 'city', 'zipcode', 'state']
