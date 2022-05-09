from django.contrib.auth import authenticate, get_user_model, login, logout
from django.http import request
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.urls.base import reverse
from django.views.generic import View, FormView, CreateView
from .auth_forms import LoginPasswordForm, MobileForm, RegisterForm
from .models import Referral
User = get_user_model()

   

class GetPhoneView(FormView):
    template_name = 'users/auth/get-phone.html'
    form_class = MobileForm


    def form_valid(self, form):
        mobile = form.cleaned_data['mobile']
        self.request.session['mobile'] = mobile
        if User.objects.filter(mobile=mobile).exists():
            return redirect(reverse('auth:login_password'))
        return redirect(reverse('auth:register'))

class LoginPasswordView(FormView):
    template_name = 'users/auth/login-password.html'

    def get(self, request, *args: str, **kwargs):
        self.mobile = self.request.session.get('mobile')
        if not self.mobile:
            return redirect(reverse('auth:get_phone'))
        self.user = User.objects.filter(mobile=self.mobile).first()
        if not self.user:
            return redirect(reverse('auth:get_phone'))
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mobile'] = self.mobile
        context['display_name'] = self.user.display_name
        return context

    def get_form(self):
        self.mobile = self.request.session.get('mobile')
        self.user = User.objects.filter(mobile=self.mobile).first()
        return LoginPasswordForm(request=self.request, instance=self.user, **self.get_form_kwargs())

    def form_valid(self, form):
        login(self.request, form.get_user())
        del self.request.session['mobile']
        return HttpResponseRedirect(reverse('users:dashboard'))

    def form_invalid(self, form):
        return super().form_invalid(form)

        
class RegisterView(FormView):
    template_name = 'users/auth/register.html'
    success_url = reverse_lazy('users:dashboard')
    form_class = RegisterForm

    def get(self, request, *args: str, **kwargs):
        mobile = self.request.session.get('mobile')
        if not mobile:
            return redirect(reverse('auth:get_phone'))
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mobile'] = self.request.session.get('mobile')
        return context

    def form_valid(self, form):
        mobile = self.request.session.get('mobile')
        user = form.save(mobile=mobile)
        if form.referrer:
            Referral.objects.create(referred=user, referrer=form.referrer)
        login(self.request, user)
        del self.request.session['mobile']
        return super().form_valid(form)

class LogoutView(View):
    def get(self, request, *args: str, **kwargs):
        logout(request)
        return redirect(reverse('users:dashboard'))

