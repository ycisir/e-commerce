from django.shortcuts import render
from django.views import View
from product.models import Product

class HomeView(View):
    def get(self, request):
        top_wears = Product.objects.filter(category='TW')
        bottom_wears = Product.objects.filter(category='BW')
        mobiles = Product.objects.filter(category='M')
        laptops = Product.objects.filter(category='L')
        context = {
            'top_wears':top_wears, 
            'bottom_wears':bottom_wears, 
            'mobiles':mobiles, 
            'laptops':laptops
        }
        return render(request, 'core/home.html', context)
