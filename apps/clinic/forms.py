from django import forms
from apps.users.models import User
from apps.core import utils
from .models import (Reservation, ReservationService, ReservationMedicine,
                     ImageGallery, Medicine, Service, Brand, BrandCompany,
                     Illness
                    )


class PatientQuickForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'mobile']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        mobile = utils.persian_digits_to_english(mobile)
        return mobile


class ReservationQuickForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['patient', 'book_time', 'requested_services']

    def clean_book_time(self):
        book_time = self.cleaned_data['book_time']
        if book_time.locked:
            raise forms.ValidationError('این زمان غیرفعال شده است')
        return book_time

        
class ReservationServiceForm(forms.ModelForm):
    class Meta:
        model = ReservationService
        fields = ['service', 'brand', 'amount', 'final_price', 'description']

    def clean_price(self):
        price = self.cleaned_data['final_price']
        if price <= 0:
            raise forms.ValidationError('قیمت نمیتواند مکتر از باشد')
        return price

        
class ReservationImageForm(forms.ModelForm):
    class Meta:
        model = ImageGallery
        fields = ('image', 'description', 'capture_time')

class ReservationImageUpdateForm(forms.ModelForm):
    class Meta:
        model = ImageGallery
        fields = ('description', 'capture_time')
        
class ReservationMedicineForm(forms.ModelForm):
    class Meta:
        model = ReservationMedicine
        fields = ('medicine', 'how_to_use')

class IllnessForm(forms.ModelForm):
    class Meta:
        model = Illness
        fields = ('name', 'description')
        
        
class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ('name', 'description', 'price')
        

class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = ('name', 'brand', 'description', )
        

class BrandCompanyForm(forms.ModelForm):
    class Meta:
        model = BrandCompany
        fields = ('name', 'description')
        
        
class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ('name', 'description', 'company')

