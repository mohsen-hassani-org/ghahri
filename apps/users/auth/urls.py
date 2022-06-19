from django.urls import path
from django.contrib.auth import views as auth
from .views import StaffLoginView, StaffForgetPasswordView, StaffNewPasswordView

urlpatterns = [
    path('staff/login/', StaffLoginView.as_view(), name='staff_login'),
    path('staff/forgot-password/', StaffForgetPasswordView.as_view(), name='staff_forget_password'),
    path('staff/new-password/', StaffNewPasswordView.as_view(), name='password_reset_confirm'),
    path('logout/', auth.LogoutView.as_view(), name='account_logout'),
]
