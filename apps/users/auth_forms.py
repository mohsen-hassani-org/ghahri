from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.core.exceptions import ValidationError
from apps.core.models import Career, CareerGroup
User = get_user_model()


class MobileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('mobile', )

    def validate_unique(self) -> None:
        return


class LoginPasswordForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('mobile', 'password', )
    
    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)
        self.fields['mobile'].widget = forms.HiddenInput()
        self.error_messages = {
            'invalid_login': 'رمز وارد شده صحیح نمی‌باشد',
            'inactive': 'حساب شما مسدود شده است. جهت رفع مسدودی حساب با پشتیبانی تماس بگیرید.',
        }
        self._user = None

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not password:
            raise forms.ValidationError('رمز عبور الزامی است')
        return password

    def clean(self):
        mobile = self.cleaned_data.get('mobile')
        password = self.cleaned_data.get('password')

        if mobile is not None and password:
            __user = User.objects.get_user_by_mobile(mobile)
            __user = authenticate(self.request, username=__user.username, password=password)
            if __user is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(__user)
            self._user = __user

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )

    def get_invalid_login_error(self):
        return ValidationError(
            self.error_messages['invalid_login'],
            code='invalid_login',
            params={'mobile': 'موبایل'},
        )

    def get_user(self):
        return self._user


class RegisterForm(forms.ModelForm):
    referrer_code = forms.CharField(max_length=10,
                                    label='کد معرف',
                                    required=False)
    password = forms.CharField(widget=forms.PasswordInput,
                               label='رمز ورود',
                               required=True)
    password_confirm = forms.CharField(widget=forms.PasswordInput,
                                       label='تکرار رمز ورود', required=True)
    career_group = forms.ModelChoiceField(queryset=CareerGroup.objects.all(),
                                          empty_label='گروه شغلی',
                                          required=False,
                                          label='گروه شغلی')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'password', 'password_confirm', 
                  'referrer_code', 'career', 'career_group')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['placeholder'] = field.label
        self.referrer = None
        career_group_choices = CareerGroup.objects.all().values_list('id', 'name')
        career_group_choices = [(0, 'گروه شغلی')] + list(career_group_choices)
        if not self.is_bound:
            self.fields['career'].widget.choices.queryset = Career.objects.none()
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['career'].required = True

    def clean_career(self):
        career = self.cleaned_data.get('career')
        if not career:
            raise forms.ValidationError('شغل الزامی است')
        return career

    def clean_referrer_code(self):
        referrer_code = self.cleaned_data['referrer_code']
        if not referrer_code:
            return ''
        referrer_code = referrer_code .upper()
        self.referrer = User.objects.filter(referral_code=referrer_code).first()
        if not self.referrer:
            raise forms.ValidationError('هیچ کاربری برای کد معرف وارد شده پیدا نشد')
        return referrer_code 

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not password:
            raise forms.ValidationError('رمز عبور الزامی است')
        if len(password) < 6:
            raise forms.ValidationError('رمز عبور باید حداقل 6 کاراکتر باشد')
        return password

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password != password_confirm:
            raise forms.ValidationError('رمز عبور با تکرار آن یکسان نیست')
        return password_confirm

        
    def save(self, mobile, commit=True):
        user = super().save(commit=False)
        user.mobile = mobile
        user.username = mobile
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

