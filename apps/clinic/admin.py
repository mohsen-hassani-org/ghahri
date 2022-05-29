from datetime import datetime
from django import forms
from django.contrib import admin
from jalali_date import date2jalali
from .models import (Medicine, Illness, Service, BookTime,
                     ReservationService, Reservation,
                     ReservationMedicine, ImageGallery,
                     BrandCompany, Brand,)


@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')
    list_filter = ('name', )


@admin.register(Illness)
class IllnessAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')
    list_filter = ('name', )


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price', )
    search_fields = ('name', 'description', 'price', )
    list_filter = ('name', )

@admin.register(BrandCompany)
class BrandCompany(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name', )


@admin.register(Brand)
class Brand(admin.ModelAdmin):
    list_display = ('name', 'company', )
    search_fields = ('name', 'company', )
    list_filter = ('name', 'company', )


@admin.register(BookTime)
class BookTimeAdmin(admin.ModelAdmin):
    list_display = ('date_jalali', 'time_in_day')
    search_fields = ('date', 'time_in_day')
    list_filter = ('date', 'time_in_day')

    def date_jalali(self, obj):
        return date2jalali(obj.date).strftime("%Y/%m/%d")
    date_jalali.short_description = 'تاریخ'


@admin.register(ReservationService)
class ReservationServiceAdmin(admin.ModelAdmin):
    list_display = ('reservation', 'service', 'service_brand', 'brand', 'service_amount', 'description', 'final_price')
    search_fields = ('reservation', 'service', 'service_brand', 'brand', 'service_amount', 'description', 'final_price')
    list_filter = ('reservation', 'service', 'service_brand', 'brand', 'service_amount', 'description', 'final_price')
    autocomplete_fields = ('reservation', 'service', 'brand')

@admin.register(ReservationMedicine)
class ReservationMedicineAdmin(admin.ModelAdmin):
    list_display = ('reservation', 'medicine', 'how_to_use')
    search_fields = ('reservation', 'medicine', 'how_to_use')
    list_filter = ('reservation', 'medicine', 'how_to_use')


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ('patient', 'book_time', )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        today = datetime.today().date()
        self.fields['book_time'].queryset = BookTime.objects.filter(
            date__gte=today,
        )
    

class ReservationServiceInline(admin.TabularInline):
    model = ReservationService
    fields = ('reservation', 'service', 'brand', 'service_amount', 'final_price')

class ReservationMedicineInline(admin.TabularInline):
    model = ReservationMedicine
    fields = ('reservation', 'medicine', 'how_to_use')

class ImageGalleryInline(admin.TabularInline):
    model = ImageGallery
    fields = ('image',)



@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    form = ReservationForm
    list_display = ('patient', 'book_time', 'visited_at')
    search_fields = ('patient', 'book_time', 'visited_at')
    list_filter = ('patient', 'book_time__date', 'visited_at')
    inlines = [ReservationServiceInline, ReservationMedicineInline,
               ImageGalleryInline, ]
    autocomplete_fields = ('patient', 'book_time', )


@admin.register(ImageGallery)
class ImageGalleryAdmin(admin.ModelAdmin):
    list_display = ('user', 'description', 'capture_time', 'reservation')
    search_fields = ('user', 'description', 'capture_time', 'reservation')
    list_filter = ('user', 'description', 'capture_time', 'reservation')
