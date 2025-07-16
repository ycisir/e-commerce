from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from customer.forms import CustomerProfileForm
from customer.models import Customer
from django.views.generic import TemplateView
from django.contrib import messages

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'customer/dashboard.html'
    def get_queryset(self):
        address = Customer.objects.filter(user=self.request.user)
        return[address]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_address'] = self.get_queryset()[0]
        return context
    



class AddressView(LoginRequiredMixin, FormView):
    template_name = 'customer/address.html'
    form_class = CustomerProfileForm
    success_url = '/customer/dashboard/'

    def form_valid(self, form):
        user = self.request.user
        customer_name = form.cleaned_data['name']
        locality = form.cleaned_data['locality']
        city = form.cleaned_data['city']
        state = form.cleaned_data['state']
        zipcode = form.cleaned_data['zipcode']
        update = Customer(user=user, name=customer_name, locality=locality, city=city, state=state, zipcode=zipcode)
        update.save()
        messages.success(self.request, 'Details added successfully!')
        return super().form_valid(form)
