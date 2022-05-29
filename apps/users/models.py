from django.templatetags.static import static
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from apps.core.models import AbstractModel
from apps.core.utils import generate_random_string
from .validators import MobileValidator, NationalCodeValidator
from .managers import CustomUserManager


def generate_referral():
    code = generate_random_string(use_lower=False, use_symbols=False, length=8)
    users_code = User.objects.values('referral_code')
    while code in users_code:
        code = generate_random_string(use_lower=False, use_symbols=False, length=8)
    return code


class User(AbstractUser, AbstractModel):
    """Custom User model"""
    class DeactivateReasons(models.IntegerChoices):
        UNKNOWN = 0, 'نامشخص'
        BY_ADMIN = 1, 'غیر فعال توسط مدیر'
        BY_STAFF = 2, 'غیر فعال توسط کارمندان'
        VERIFY_MOBILE = 3, 'عدم تایید موبایل'
        VERIFY_EMAIL = 4, 'عدم تایید ایمیل'
    
    class GenderTypes(models.IntegerChoices):
        MALE = 0, 'مرد'
        FEMALE = 1, 'زن'

    class Roles(models.IntegerChoices):
        ADMIN = 0, 'مدیر'
        DOCTOR = 1, 'دکتر'
        SECRETARY = 2, 'منشی'
        PATIENT = 3, 'بیمار'
    
    class MarriageStatuses(models.IntegerChoices):
        SINGLE = 0, 'مجرد'
        MARRIED = 1, 'متاهل'

    mobile = models.CharField('موبایل', max_length=11, unique=True,
                              help_text='موبایل باید به فرمت 09123456789 وارد شود',
                              validators=[MobileValidator()],
                              error_messages={
                                  'unique': 'این شماره موبایل از قبل در سامانه ثبت شده است',
                                },
                            )
    password = models.CharField('گذرواژه', max_length=128, null=True, blank=True)
    first_name = models.CharField(verbose_name='نام', max_length=150, blank=True)
    last_name = models.CharField(verbose_name='نام خانوادگی', max_length=150, blank=True)
    national_code = models.CharField(max_length=10, verbose_name='کد ملی',
                                     validators=[NationalCodeValidator()],
                                     null=True, blank=True, unique=True)
    career = models.ForeignKey('core.Career', on_delete=models.PROTECT, verbose_name='شغل',
                               null=True, blank=True, related_name='users')
    deactivate_reason = models.PositiveSmallIntegerField(choices=DeactivateReasons.choices,
                                                         default=DeactivateReasons.UNKNOWN,
                                                         verbose_name='غیرفعال به دلیل')
    email = models.EmailField(unique=True, null=True, blank=True, verbose_name='ایمیل')
    address = models.TextField(verbose_name='آدرس', null=True, blank=True)
    birth_date = models.DateField(verbose_name='تاریخ تولد', null=True, blank=True)
    gender = models.IntegerField(verbose_name='جنسیت', null=True, blank=True, choices=GenderTypes.choices)
    role = models.IntegerField(choices=Roles.choices, default=Roles.PATIENT, verbose_name='نقش')
    marriage_status = models.IntegerField(choices=MarriageStatuses.choices,
                                            default=MarriageStatuses.SINGLE,
                                            verbose_name='وضعیت تاهل')
    phone_number = models.CharField(max_length=15, verbose_name='شماره تلفن ثابت', null=True, blank=True)
    current_illness = models.ManyToManyField('clinic.Illness', verbose_name='بیماری های فعلی',
                                                related_name='patients', blank=True)
    current_medicines = models.TextField(verbose_name='داروهای مصرفی فعلی', null=True, blank=True)
    treatment_history = models.TextField(verbose_name='سوابق درمانی', null=True, blank=True)
    notes = models.TextField(verbose_name='یادداشت', null=True, blank=True)
    referral_code = models.CharField(verbose_name='کد معرف', max_length=10, default=None, unique=True, null=True)
    objects = CustomUserManager()

    REQUIRED_FIELDS = ["mobile", ]

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربر'
        ordering = ('-id',)

    def __str__(self):
        role = self.get_role_display()
        return f'{self.display_name} ({role})'

    def get_absolute_url(self):
        return reverse('users:user_details', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        if self.email == '':
            self.email = None
        if not self.referral_code:
            self.referral_code = generate_referral()
        if self.role in [self.Roles.SECRETARY, self.Roles.DOCTOR, self.Roles.ADMIN]:
            self.is_staff = True
        if self.role == self.Roles.ADMIN:
            self.is_superuser = True
        super().save(*args, **kwargs)

    @property
    def display_name(self) -> str:
        return (
            self.first_name + ' ' + self.last_name
            if self.first_name and self.last_name
            else self.mobile
        )

    @property
    def avatar_url(self) -> str:
        if self.avatar:
            return self.avatar.url
        f = static('account/profile.png')
        return f

    def deactivate(self, reason: DeactivateReasons) -> None:
        """Deactivate user by reason

        DO NOT explicitly set users is_active field without saving the reason why it is deactivated
        """
        self.deactivate_reason = reason
        self.is_active = False
        self.save()

    def activate(self) -> None:
        """Activate user

        Will change user's deactivate reason to UNKNOWN
        """
        self.deactivate_reason = self.DeactivateReasons.UNKNOWN
        self.is_active = True
        self.save()

    @property
    def total_referred_users(self):
        return self.referrals.count()


class Referral(AbstractModel):
    referred = models.OneToOneField(User, verbose_name='گاربر معرفی شده',
                                    on_delete=models.PROTECT, unique=True,
                                    related_name='referral_by')
    referrer = models.ForeignKey(User, verbose_name='ارجاع دهنده',
                                 on_delete=models.PROTECT,
                                 related_name='referrals')





# class AuthSMSRequest(models.Model):
#     class Meta:
#         verbose_name = 'درخواست احراز هویت پیامکی'
#         verbose_name_plural = 'درخواست احراز هویت پیامکی'
#         ordering = ('-id', )

#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
#                              verbose_name='کاربر', null=True, blank=True)
#     mobile = models.CharField('موبایل', max_length=11, help_text=('نمونه: 09123456789'),
#                               validators=[MobileValidator()])
#     sms_code = models.CharField('کد پیامکی', max_length=5, null=True, blank=True)
#     created_at = models.DateTimeField('تاریخ ثبت', auto_now_add=True)
#     updated_at = models.DateTimeField('تاریخ بروزرسانی', auto_now=True)

#     def __str__(self):
#         return self.mobile

#     def login_user(self, request):
#         user = self.user
#         if not user:
#             return
#         login(request, user)

#     def generate_sms_code(self):
#         self.sms_code = generate_sms_code()
#         self.save()

#     def send_code(self):
#         print(f'>>>>>>>>>>>>>{self.sms_code}<<<<<<<<<<<<<<<')
