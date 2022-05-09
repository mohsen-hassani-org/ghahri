from django.urls import path
from apps.users.views import DashboardView, UserUpdateView


app_name = 'users'

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('profile/', DashboardView.as_view(), name='profile'),
    path('profile/update/', UserUpdateView.as_view(), name='update_profile'),
]
