from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext_lazy as _
from django.views.generic import View, FormView, CreateView, UpdateView
from apps.users.forms import UserForm
from apps.core.base import BaseContextMixin, GenericFormView, GenericModelFormView
User = get_user_model()

# Create your views here.
class DashboardView(LoginRequiredMixin, BaseContextMixin, View):
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return render(request, 'users/dashboard.html', context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class UserUpdateView(LoginRequiredMixin, GenericModelFormView):
    model = User
    form_class = UserForm
    template_name = 'generic_model_form.html'
    success_url = reverse_lazy('users:dashboard')
    success_message = 'اطلاعات شما با موفقیت بروزرسانی شد.'

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['extra_scripts'] = ['users/scripts/career_dropdown.js']
        return context
