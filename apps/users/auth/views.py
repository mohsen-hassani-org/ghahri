from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.views.generic import View, TemplateView, FormView
from django.contrib.auth.signals import user_logged_in


User = get_user_model()


class StaffLoginView(FormView):
    pass


class StaffForgetPasswordView(FormView):
    pass


class StaffNewPasswordView(FormView):
    pass