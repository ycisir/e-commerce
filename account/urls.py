from django.urls import path
from account import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('register/', views.RegistrationView.as_view(), name='register'),
    path('activate/<str:uidb64>/<str:token>/', views.activate_account, name='activate'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('password_change/', views.CustomPasswordChangeView.as_view(), name='password_change'),
    path('password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset_confirm/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('dashboard/', views.ProfileView.as_view(), name='dashboard'),
    path('address/', views.AddressView.as_view(), name='address'),
]