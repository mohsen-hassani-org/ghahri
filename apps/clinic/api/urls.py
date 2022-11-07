from django.urls import path, include
from rest_framework import routers
from .views import QuickCreateReservationApiView, QuickCreatePatientApiView, ConfirmMobileViewSet, WorkSampleApiView


clinic_router = routers.DefaultRouter()
clinic_router.register('confirm-mobile', ConfirmMobileViewSet, basename='confirm_mobile')


urlpatterns = [
    path('user/create/', QuickCreatePatientApiView.as_view(), name='api_user_create'),
    path('reservation/create/', QuickCreateReservationApiView.as_view(), name='api_reservation_create'),
    path('', include(clinic_router.urls)),
    path('clinic/patients/', WorkSampleApiView.as_view(), name='api_work_sample'),
]