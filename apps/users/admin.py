from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User 
from jalali_date.admin import ModelAdminJalaliMixin
from django.contrib.auth.forms import (
    UserChangeForm,
    UserCreationForm,
)

class CustomUserCreationForm(UserCreationForm):
    password1 = None
    password2 = None

    def save(self, commit=True):
        self.cleaned_data["password1"] = None
        return super().save(commit=False)


@admin.register(User)
class CustomUserAdmin(ModelAdminJalaliMixin, UserAdmin):
    list_display = ('mobile', 'username', 'first_name', 'last_name', 'is_staff', 'email')
    search_fields = ('mobile', 'username', 'first_name', 'last_name', 'email', 'notes')
    fieldsets = (
        (None, {'fields': ('mobile', 'username', 'password')}),
        ('اطلاعات فردی', {'fields': ('first_name', 'last_name', 'email', 'notes',
                                     'national_code', 'birth_date', 'career',
                                     'address', 'marriage_status', 'phone_number')}),
        ('دسترسی‌ها', {'fields': ('role',)}),
        ('اطلاعات پزشکی', {'fields': ('current_illness', 'current_medicines', 'treatment_history')}),
        ("تاریخ‌های مهم", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'mobile', 'username',
                       'role', 'national_code', 'career', 'gender',
                       'address', 'birth_date', 'marriage_status',
                       'phone_number', 'current_illness', 'current_medicines',
                       'treatment_history', 'notes'
                       )}
         ),
    )
    autocomplete_fields = ('career',)
    add_form = CustomUserCreationForm
    filter_horizontal = ('current_illness',) 
