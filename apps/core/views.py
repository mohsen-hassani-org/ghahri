from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.http import JsonResponse
from apps.core.models import UserAlert
from apps.core.base import GenericModelListView
from .models import CareerGroup

# Create your views here.

class AlertListView(LoginRequiredMixin, GenericModelListView):
    page_title = 'هشدارها'
    fields = ['alert__title', 'alert__body', 'created_at']
    field_labels = {
        'created_at': 'ایجاد شده در'
    }
    datetime_fields = ['created_at']

    def get_queryset(self):
        return UserAlert.objects.filter(user=self.request.user)

class CareerGroupJobsAjaxView(View):
    def get(self, request, *args: str, **kwargs):
        group_id = self.kwargs.get('group_id')
        careers = CareerGroup.objects.get(pk=group_id).careers.values_list('id', 'name')
        return JsonResponse({'careers': list(careers)})
