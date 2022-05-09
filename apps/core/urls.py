from django.urls import path
from .views import AlertListView, CareerGroupJobsAjaxView
app_name = 'core'

urlpatterns = [
    path('alerts/', AlertListView.as_view(), name='alerts'),
    path('careers/<group_id>/', CareerGroupJobsAjaxView.as_view(), name='careers'),
]
