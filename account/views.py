from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic.edit import FormView
from account.forms import RegistrationForm, LoginForm, CustomPasswordChangeForm, PasswordResetForm, CustomSetPasswordForm
from account.models import User
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.conf import settings
from django.urls import reverse
from account.utils import send_activation_email, send_reset_password_email
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

class RegistrationView(FormView):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_customer:
                return redirect('customer_dashboard')
            else:
                return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    form_class = RegistrationForm
    template_name = 'account/register.html'
    
    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.is_active = False #account inactive until email is verified
        user.save()

        # send activation link
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        activation_link = reverse('activate', kwargs={'uidb64': uidb64, 'token': token})
        activation_url = f'{settings.SITE_DOMAIN}{activation_link}'

        send_activation_email(user.email, activation_url)

        messages.success(self.request, 'Registration successfull please check your email to activate your account!')
    
        return redirect('login')


def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)


        # check if account already activate
        if user.is_active:
            messages.warning(request, 'This account has already been activated!')
            return redirect('login')
        
        if default_token_generator.check_token(user, token):
            user.is_active = True #activate account
            user.save()
            messages.success(request, 'Your account has been activated successfully!')
            return redirect('login')
        else:
            messages.error(request, 'The activation link in invalid or has expired!')
            return redirect('login')
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        messages.error(request, 'Invalid activation link!')
        return redirect('login')
        

class LoginView(View):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_customer:
                return redirect('customer_dashboard')
            else:
                return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    
    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, 'account/login.html', {'form': form})

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            messages.error(request, 'Both fields are required!')
            return redirect('login')
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'Invalid email or password!')
            return redirect('login')
        

        if user is not None:
            if not user.is_active:
                messages.error(request, 'Your account is inactive please activate your account')
                return redirect('login')
        
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)

            if user.is_customer:
                messages.success(request, 'Logged in successfully')
                return redirect('customer_dashboard')
            else:
                messages.error(request, 'You do not have permission to access this area!')
                return redirect('home')
        else:
            messages.error(request, 'Invalid email or password!')
            return redirect('login')



class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'account/password_change.html'
    success_url = '/account/login/'
    form_class = CustomPasswordChangeForm
    
    def form_valid(self, form):
        response =  super().form_valid(form)
        logout(self.request)
        messages.success(self.request, 'Password change successfully, please login with new password')
        return response
    
    # def form_invalid(self, form):
    #     # messages.error(self.request, 'There was an error in changing your password, please try again!')
    #     return super().form_invalid(form)



class PasswordResetView(FormView):
    template_name = 'account/password_reset.html'
    form_class = PasswordResetForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        user = User.objects.get(email=email)

        if user:
            reset_url = self.get_reset_url(user)
            send_reset_password_email(user.email, reset_url)
            messages.success(self.request, 'We have sent a password link please check your email!')

        return super().form_valid(form)
    
    # def form_invalid(self, form):
    #     messages.error(self.request, 'No account exist with this email!')
    #     return super().form_invalid(form)
    
    def get_reset_url(self, user):
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        reset_url = reverse_lazy('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})

        return f"{self.request.build_absolute_uri(reset_url)}"



class PasswordResetConfirmView(View):
    template_name = 'account/password_reset_confirm.html'

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)

            if default_token_generator.check_token(user, token):
                form = CustomSetPasswordForm(user=user)
                context = {
                    'form': form,
                    'uidb64': uidb64,
                    'token': token
                }
                return render(request, self.template_name, context)
            else:
                messages.error(request, 'This link has expired or invalid!')
                return redirect('password_reset')
        except Exception as e:
            messages.error(request, 'An error occured please try again latter!')
            return redirect('password_reset')
        
    def post(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)

            if default_token_generator.check_token(user, token):
                form = CustomSetPasswordForm(user=user, data=request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Your password has been successfully reset')
                    return redirect('login')
                else:
                    for field, errors in form.errors.items():
                        for error in errors:
                            messages.error(request, error)
                    context = {
                        'form': form,
                        'uidb64': uidb64,
                        'token': token
                    }
                    return render(request, self.template_name, context)
            else:
                messages.error(request, 'This link has expired or invalid!')
                return redirect('password_reset')
        except Exception as e:
            messages.error(request, 'An error occured please try again latter!')
            return redirect('password_reset')