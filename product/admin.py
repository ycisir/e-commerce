from django.contrib import admin
from product.models import Product

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'selling_price', 'discount_price', 
                    'description', 'brand', 'category', 'product_image']
