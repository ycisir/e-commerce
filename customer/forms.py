from django import forms
from customer.models import Customer

class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['customer_name', 'locality', 'city', 'state', 'zipcode']
        widgets = {
            'customer_name': forms.TextInput(attrs={'class': 'form-control'}),
            'locality': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.Select(attrs={'class': 'form-control'}),
            'zipcode': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
    	super().__init__(*args, **kwargs)
    	self.fields['customer_name'].label_suffix = ''
    	self.fields['locality'].label_suffix = ''
    	self.fields['city'].label_suffix = ''
    	self.fields['state'].label_suffix = ''
    	self.fields['zipcode'].label_suffix = '' 