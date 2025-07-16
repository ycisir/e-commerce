from django.shortcuts import render
from django.views import View
from product.models import Product

class ProductDetailView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        in_cart = False
        if request.user.is_authenticated:
            # in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
            context = {'product':product, 'in_cart':in_cart}
            return render(request, 'product/product_detail.html', context)
        # print(in_cart)
        context = {'product':product, 'in_cart':in_cart}
        return render(request, 'product/product_detail.html', context)
