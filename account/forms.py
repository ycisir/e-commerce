from django import forms
from account.models import User, Customer
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm


class RegistrationForm(forms.ModelForm):
	password = forms.CharField(
		min_length=6, 
		widget=(forms.PasswordInput(attrs={'class': 'form-control'})), 
		label_suffix=''
	)
	
	confirm_password = forms.CharField(
		widget=(forms.PasswordInput(attrs={'class': 'form-control'})), 
		label_suffix=''
	)

	class Meta:
		model = User
		fields = ('email', 'password', 'confirm_password')
		widgets = {
			'email': forms.EmailInput(attrs={
				'class': 'form-control',
			})
		}

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['email'].label = 'Email address'
		self.fields['email'].label_suffix = ''

	def clean(self):
		cleaned_data = super().clean()
		password = cleaned_data.get('password')
		confirm_password = cleaned_data.get('confirm_password')

		if password and confirm_password and password != confirm_password:
			self.add_error('confirm_password', 'Password and confirm password do not match!')
		
		return cleaned_data

	def clean_email(self):
		email = self.cleaned_data.get('email')

		if User.objects.filter(email=email).exists():
			raise forms.ValidationError('A user with this email already exists!')

		return email


class LoginForm(forms.Form):
	email = forms.CharField(widget=forms.EmailInput(attrs={'class':'form-control'}), label_suffix='', required=True)
	password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}), label_suffix='', required=True)


class PasswordResetForm(forms.Form):
	email = forms.EmailField(error_messages={'required': 'Email required'},widget=forms.EmailInput(attrs={'class':'form-control'}), label_suffix='')

	def clean_email(self):
		email = self.cleaned_data.get('email')

		if not User.objects.filter(email=email).exists():
			raise forms.ValidationError('No account is associated with this email address!')

		return email



class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control'})
        self.fields['old_password'].widget.label_suffix = ''
        self.fields['new_password1'].widget.label_suffix = ''
        self.fields['new_password2'].widget.label_suffix = ''
        self.fields['new_password2'].label = 'Confirm New Password'


class CustomSetPasswordForm(SetPasswordForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['new_password1'].widget.attrs.update({'class': 'form-control'})
		self.fields['new_password2'].widget.attrs.update({'class': 'form-control'})
		self.fields['new_password2'].label = 'Confirm New Password'
		self.fields['new_password1'].label_suffix = ''
		self.fields['new_password2'].label_suffix = ''




class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'locality', 'city', 'state', 'zipcode']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'locality': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.Select(attrs={'class': 'form-control'}),
            'zipcode': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
    	super().__init__(*args, **kwargs)
    	self.fields['name'].label_suffix = ''
    	self.fields['locality'].label_suffix = ''
    	self.fields['city'].label_suffix = ''
    	self.fields['state'].label_suffix = ''
    	self.fields['zipcode'].label_suffix = '' 