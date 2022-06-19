from secrets import choice
from django import forms
from django_filters import FilterSet
from django.contrib.auth import get_user_model
from apps.core import utils
from apps.core.models import CareerGroup, Career
User = get_user_model()


class UserForm(forms.ModelForm):
    password_confirm = forms.CharField(
        label='تکرار رمز عبور',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    password= forms.CharField(
        label='رمز عبور',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'mobile', 'role', 'avatar', 'password', 'password_confirm']

    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        mobile = utils.persian_digits_to_english(mobile)
        return mobile

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise forms.ValidationError('رمز عبور باید حداقل 8 کاراکتر باشد')
        if password.isdigit():
            raise forms.ValidationError('رمز عبور نمیتواند تنها شامل عدد باشد')
        return password

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if not password:
            return password_confirm
        if password != password_confirm:
            raise forms.ValidationError('رمز عبور و تکرار آن باید یکسان باشد')
        return password_confirm

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['role'].widget.choices = self.remove_patient_from_roles(User.Roles.choices)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        
    @staticmethod
    def remove_patient_from_roles(choices):
        patient = (
            User.Roles.PATIENT.value,
            User.Roles.PATIENT.label,
        )
        choices.remove(patient)
        return choices

        
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'mobile', 'role', 'avatar']

    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        mobile = utils.persian_digits_to_english(mobile)
        return mobile

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['role'].widget.choices = UserForm.remove_patient_from_roles(User.Roles.choices)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
 
        
class UserSetPasswordForm(forms.ModelForm):
    password_confirm = forms.CharField(
        label='تکرار رمز عبور',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    password= forms.CharField(
        label='رمز عبور',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )


    class Meta:
        model = User
        fields = ['password', 'password_confirm']

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise forms.ValidationError('رمز عبور باید حداقل 8 کاراکتر باشد')
        if password.isdigit():
            raise forms.ValidationError('رمز عبور نمیتواند تنها شامل عدد باشد')
        return password

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if not password:
            return password_confirm
        if password != password_confirm:
            raise forms.ValidationError('رمز عبور و تکرار آن باید یکسان باشد')
        return password_confirm


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'avatar', )
            
class UserSignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'mobile', )


class PatientFilterForm(FilterSet):
    class Meta:
        model = User
        fields = {
            'first_name': ['icontains'], 
            'last_name': ['icontains'], 
            'mobile': ['icontains'],
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form.fields['first_name__icontains'].label = 'نام'
        self.form.fields['last_name__icontains'].label = 'نام خانوادگی'
        self.form.fields['mobile__icontains'].label = 'موبایل'
        


class PatientForm(forms.ModelForm):
    career_group = forms.ModelChoiceField(
        queryset=CareerGroup.objects.all(),
        required=False,
        empty_label='گروه شغلی',
        label='گروه شغلی'
    )
        
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'mobile', 'national_code',
                  'career_group', 'career', 'birth_date', 'address', 'gender',
                  'marriage_status', 'phone_number', 'current_illness', 
                  'current_medicines', 'treatment_history', 'notes')

    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        mobile = utils.persian_digits_to_english(mobile)
        return mobile

