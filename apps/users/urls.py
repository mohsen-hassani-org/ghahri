from django.urls import include, path
from apps.users.views import (
    DashboardView, ProfileUpdateView, PatientCreateView, PatientDetailView,
    PatientListView, PatientEditView, UserListView, UserUpdateView,
    UserCreateView, UserSetPasswordView,
)


app_name = 'users'

urlpatterns = [
    path('', UserListView.as_view(), name='user_list'),
    path('new/', UserCreateView.as_view(), name='new_user'),
    path('<pk>/update/', UserUpdateView.as_view(), name='update_user'),
    path('<pk>/set-password/', UserSetPasswordView.as_view(), name='set_password'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('profile/', DashboardView.as_view(), name='profile'),
    path('profile/update/', ProfileUpdateView.as_view(), name='update_profile'),
    path('auth/', include('apps.users.auth.urls')),
    path('patients/', PatientListView.as_view(), name='patient_list'),
    path('patients/new/', PatientCreateView.as_view(), name='patient_create'),
    path('patients/<pk>/', PatientDetailView.as_view(), name='patient_details'),
    path('patients/<pk>/edit/', PatientEditView.as_view(), name='patient_edit'),
]
