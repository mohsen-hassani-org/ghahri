from django.urls import path
from apps.users.auth_views import GetPhoneView, LoginPasswordView, RegisterView, LogoutView
from django.contrib.auth import views as auth_views


app_name = 'auth'

urlpatterns = [
    path('phone/', GetPhoneView.as_view(), name='get_phone'),
    path('register/', RegisterView.as_view(), name='register'),
    # path('login/code/', LoginCodeView.as_view(), name='login_code'),
    # path('login/password/', LoginPasswordView.as_view(), name='login_password'),
    path('login/', LoginPasswordView.as_view(), name='login_password'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
