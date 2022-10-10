from urllib import request
from django.contrib.auth import update_session_auth_hash
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext_lazy as _
from django.views.generic import View, ListView, CreateView, UpdateView, TemplateView, FormView
from jalali_date import date2jalali, datetime2jalali
from apps.core.permissions import PermissionRequireMixin, Permissions
from apps.core.base import BaseContextMixin, GenericFormView, GenericModelFormView
from apps.core.mixins import CustomFormTemplateMixin, CustomListTemplateMixin
from .forms import (
    PatientForm, UserForm, PatientFilterForm, UserSignUpForm, UserProfileForm,
    UserUpdateForm, UserSetPasswordForm
)
User = get_user_model()


class DashboardView(LoginRequiredMixin, BaseContextMixin, View):
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return render(request, 'users/dashboard.html', context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ProfileUpdateView(LoginRequiredMixin, GenericModelFormView):
    model = User
    form_class = UserProfileForm
    template_name = 'generic_model_form.html'
    success_url = reverse_lazy('users:dashboard')
    success_message = 'اطلاعات شما با موفقیت بروزرسانی شد.'

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['extra_scripts'] = ['users/scripts/career_dropdown.js']
        return context

        
class UserListView(CustomListTemplateMixin, PermissionRequireMixin, ListView):
    permissions = [User.Roles.DOCTOR, User.Roles.ADMIN]
    page_title = 'لیست کاربران'
    queryset = User.objects.filter(role__in=[User.Roles.DOCTOR, User.Roles.SECRETARY, User.Roles.ADMIN])
    context_object_name = 'users'
    paginate_by = 100
    ordering = '-created_at'
    fields = ['username', 'first_name', 'last_name', 'role', 'created_at', 'last_login']
    header_buttons = [{'title': 'افزودن کاربر', 'url': reverse_lazy('users:new_user')}]
    action_buttons = [
        {'title': 'ویرایش', 'url_name': 'users:update_user', 'arg_field': 'id',
         'fa-icon': 'fa-edit', 'class': '', 'class_form_field': 'id'},
        {'title': 'تغییر رمز', 'url_name': 'users:set_password', 'arg_field': 'id',
         'fa-icon': 'fa-edit', 'class': 'btn-warning', 'class_form_field': 'id'},
    ]

    def get_role(self, obj):
        return obj.get_role_display()

    def get_created_at(self, obj):
        return datetime2jalali(obj.created_at).strftime('%Y/%m/%d %H:%M:%S')

    def get_last_login(self, obj):
        last_login = obj.last_login
        if last_login:
            return datetime2jalali(last_login).strftime('%Y/%m/%d %H:%M:%S')
        return '-'


class UserCreateView(CustomFormTemplateMixin, PermissionRequireMixin, CreateView):
    permissions = [User.Roles.DOCTOR, User.Roles.ADMIN]
    model = User
    form_class = UserForm
    page_title = 'افزودن کاربر جدید'
    success_url = reverse_lazy('users:user_list')
    cancel_url = reverse_lazy('users:user_list')
    success_message = ' کاربر جدید با موفقیت ثبت شد.'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.username = user.mobile
        user.save()
        return super().form_valid(form)



class UserUpdateView(UserCreateView, UpdateView):
    page_title = 'ویرایش کاربر'
    success_message = 'کاربر با موفقیت ویرایش شد.'
    form_class = UserUpdateForm

    def get_success_url(self) -> str:
        return reverse_lazy('clinic:clinic')

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.id)


class UserSetPasswordView(CustomFormTemplateMixin, PermissionRequireMixin, FormView):
    model = User
    form_class = UserSetPasswordForm
    success_url = reverse_lazy('clinic:clinic')
    success_message = 'رمز عبور با موفقیت بروزرسانی شد.'
    page_title = 'تغییر رمز عبور'

    def get_form_kwargs(self):
        kwargs = super(UserSetPasswordView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def get_page_subtitle(self):
        user = self.get_object()
        return user.get_full_name()      

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        return get_object_or_404(User, pk=pk)
    
    def form_valid(self, form):
        user = self.get_object()
        user.set_password(form.cleaned_data['password'])
        update_session_auth_hash(self.request, user)
        user.save()
        return super().form_valid(form)


class PatientCreateView(CustomFormTemplateMixin, PermissionRequireMixin, CreateView):
    permissions = [User.Roles.SECRETARY, User.Roles.DOCTOR, User.Roles.ADMIN]
    model = User
    form_class = PatientForm
    success_url = reverse_lazy('users:patient_list')
    success_message = 'اطلاعات با موفقیت ثبت شد.'
    page_title = 'افزودن پرونده جدید'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['extra_scripts'] = ['users/scripts/career_dropdown.js']
        return context

    def form_valid(self, form):
        form.instance.role = User.Roles.PATIENT
        messages.success(self.request, self.success_message)
        return super().form_valid(form)


class PatientEditView(CustomFormTemplateMixin, PermissionRequireMixin, UpdateView):
    permissions = [User.Roles.SECRETARY, User.Roles.DOCTOR, User.Roles.ADMIN]
    model = User
    form_class = PatientForm
    success_url = reverse_lazy('users:patient_list')
    success_message = 'اطلاعات با موفقیت بروزرسانی شد.'
    page_title = 'ویرایش پرونده'

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super().form_valid(form)


class PatientListView(CustomListTemplateMixin, PermissionRequireMixin, ListView):
    permissions = [User.Roles.SECRETARY, User.Roles.DOCTOR, User.Roles.ADMIN]
    template_name = 'generic_model_list.html'
    context_object_name = 'patients'
    page_title = "لیست بیماران"
    fields = ['first_name', 'last_name', 'mobile', ]
    header_buttons = [
        {'title': 'افزودن بیمار', 'url': reverse_lazy('users:patient_create'), 'fa-icon': 'fa-plus', 'class': 'btn-success'},
    ]
    action_buttons = [
        {'title': 'مشاهده پرونده', 'url_name': 'users:patient_details', 'arg_field': 'id',
         'fa-icon': 'fa-list', 'class': '', 'class_form_field': 'id'},
        {'title': 'ویرایش', 'url_name': 'users:patient_edit', 'arg_field': 'id',
         'fa-icon': 'fa-list', 'class': '', 'class_form_field': 'id'},
    ]
    paginate_by = None
    filter_class = PatientFilterForm

    def get_queryset(self):
        objects = User.objects.filter(role=User.Roles.PATIENT)
        filtered_objects = self.filter_class(self.request.GET, queryset=objects)
        return filtered_objects.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class PatientDetailView(PermissionRequireMixin ,TemplateView):
    permissions = [User.Roles.DOCTOR, User.Roles.ADMIN, User.Roles.SECRETARY]
    template_name = 'users/patient_detail_view.html'
    context_object_name = 'patient'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        patient = get_object_or_404(User, id=kwargs['pk'])
        context["patient"] = patient
        return context




