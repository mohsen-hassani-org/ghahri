from django import forms
from django.contrib.auth import get_user_model
from apps.core.models import CareerGroup, Career
User = get_user_model()


class UserForm(forms.ModelForm):
    career_group = forms.ModelChoiceField(
        queryset=CareerGroup.objects.all(),
        required=False,
        empty_label='گروه شغلی',
        label='گروه شغلی'
    )
        
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'national_code', 'email',
                  'career_group', 'career')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.is_bound and not self.instance.career:
            empty_careers = Career.objects.none()
            self.fields['career'].widget.choices.queryset = empty_careers
        self.fields['career'].required = True
