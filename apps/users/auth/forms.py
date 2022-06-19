from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm

User = get_user_model()

class ForgetPasswordForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.CharField(attrs={'placeholder': 'شماره تماس',
                                                            'class': 'form-control'}),
                             label='شماره تماس')

class ResetPasswordForm(SetPasswordForm):
    # TODO
    pass