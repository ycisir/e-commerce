from django.urls import path
from customer import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('dashboard/', views.DashboardView.as_view(), name='customer_dashboard'),
    path('address/', views.AddressView.as_view(), name='address'),
    path('logout/', LogoutView.as_view(), name='logout'),
]