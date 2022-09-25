from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import View, TemplateView, ListView, CreateView, UpdateView, DeleteView
from jalali_date import date2jalali, jdatetime
from apps.core.permissions import PermissionRequireMixin, Permissions
from apps.core.mixins import CustomDeleteMixin, CustomListTemplateMixin, CustomFormTemplateMixin
from .models import (
    Reservation, BookTime, ReservationService, Service, ReservationMedicine,
    ImageGallery, Illness, Medicine, Brand, BrandCompany
)
from .forms import (
    ReservationQuickForm, PatientQuickForm, ReservationServiceForm,
    ReservationImageForm, ReservationMedicineForm, ServiceForm, BrandForm,
    BrandCompanyForm, IllnessForm, MedicineForm, ReservationImageUpdateForm
)


User = get_user_model()


class BookTimeCreateView(PermissionRequireMixin, View):
    permissions = [User.Roles.SECRETARY, User.Roles.DOCTOR, User.Roles.ADMIN]
    def get(self, request, *args, **kwargs):
        date = request.GET.get('date')
        try:
            date = datetime.strptime(date, '%Y-%m-%d')
        except (ValueError, TypeError):
            date = datetime.now().today() 
        BookTime.objects.create_whole_date_times(date)
        return redirect('admin:clinic_booktime_changelist')


class ClinicView(PermissionRequireMixin, TemplateView):
    template_name = 'clinic_view.html'
    permissions = [User.Roles.SECRETARY, User.Roles.ADMIN, User.Roles.DOCTOR]

    def get_date(self):
        try:
            year = int(self.request.GET.get('year'))
            month = int(self.request.GET.get('month'))
            day = int(self.request.GET.get('day'))
            jdate= jdatetime.date(year=year, month=month, day=day)
            return jdate.togregorian()
        except (ValueError, TypeError):
            return datetime.now().date()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        date = self.get_date()
        times = BookTime.objects.filter(date=date, locked=False)
        context["times"] = BookTime.objects.get_services_for_date(date)
        context["selected_date"] = {
            'date': date.strftime('%Y/%m/%d'),
            'total': times.count(),
            'free': times.filter(reservations__isnull=True).count(),
        }
        context["available_times"] = times.order_by('time_in_day')
        context["patients"] = User.objects.filter(role=User.Roles.PATIENT)
        context["services"] = Service.objects.all()
        
        
        return context
    

class BookTimeListView(PermissionRequireMixin ,TemplateView):
    permissions = [User.Roles.SECRETARY, User.Roles.DOCTOR, User.Roles.ADMIN]
    template_name = 'reservation_time_list.html'
    context_object_name = 'reservation_times'
    paginate_by = None

    def get_start_and_end_dates(self, year, month):
        jdate_from = jdatetime.date(year=year, month=month, day=1)
        if month == 12:
            month = 1
            year = year + 1
        else:
            month = month + 1
        jdate_to = jdatetime.date(year=year, month=month, day=1)
        date_from = jdate_from.togregorian()
        date_to = jdate_to.togregorian()
        return date_from, date_to

    def get_context_data(self, **kwargs):
        try:
            year = int(self.request.GET.get('year'))
            month = int(self.request.GET.get('month'))
        except (ValueError, TypeError):
            year = jdatetime.datetime.now().year
            month = jdatetime.datetime.now().month
        date_from, date_to = self.get_start_and_end_dates(year, month) 
        book_times = BookTime.objects.get_or_create_between_dates(date_from, date_to)
        context = super().get_context_data(**kwargs)
        context['book_times'] = book_times
        context['times'] = BookTime.TimesInDay.choices
        return context

    def post(self, request, *args, **kwargs):
        try:
            year = int(request.GET.get('year'))
            month = int(request.GET.get('month'))
        except (ValueError, TypeError):
            year = jdatetime.datetime.now().year
            month = jdatetime.datetime.now().month
        date_from, date_to = self.get_start_and_end_dates(year, month) 
        data = request.POST['reservation_time_ids']
        time_ids = []
        if data:
            time_ids = map(int, data.split(','))
        BookTime.objects.lock_times_between_dates(date_from, date_to)
        BookTime.objects.unlock_times(time_ids)
        messages.success(request, 'نوبت ها با موفقیت بروزرسانی شدند.')
        return redirect(reverse('clinic:book_time_list') + '?year=' + str(year) + '&month=' + str(month))


class ReservationServiceCreateView(CustomFormTemplateMixin, PermissionRequireMixin, CreateView):
    permissions = [User.Roles.DOCTOR, User.Roles.ADMIN]
    model = ReservationService
    form_class = ReservationServiceForm
    template_name = 'generic_model_multiform.html'
    success_url = reverse_lazy('clinic:reservation_list')
    page_title = 'افزودن سرویس جدید'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = Service.objects.all()
        return context

    def get_success_url(self):
        patient = self.object.reservation.patient
        return reverse('users:patient_details', kwargs={'pk': patient.id})
        

    def form_valid(self, form):
        service = form.save(commit=False)
        service.staff = self.request.user
        service.reservation_id = self.kwargs['pk']
        service.save()
        return super().form_valid(form)

 
class ReservationImageCreateView(CustomFormTemplateMixin, PermissionRequireMixin, CreateView):
    permissions = [User.Roles.DOCTOR, User.Roles.ADMIN]
    model = ImageGallery
    form_class = ReservationImageForm
    page_title = 'افزودن تصویر جدید'

    def get_reservation(self):
        id = self.kwargs['pk']
        return Reservation.objects.get(id=id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_file_form'] = True
        return context

    def get_success_url(self):
        patient = self.object.reservation.patient
        return reverse('users:patient_details', kwargs={'pk': patient.id})
        

    def form_valid(self, form):
        obj = self.get_reservation()
        image = form.save(commit=False)
        image.user = obj.patient
        image.reservation = obj
        image.save()
        return super().form_valid(form)


class ReservationImageUpdateView(ReservationImageCreateView, UpdateView):
    form_class = ReservationImageUpdateForm
    page_title = 'ویرایش تصویر'
    success_message = 'تصویر با موفقیت ویرایش شد.'

    def form_valid(self, form):
        form.save()
        self.show_success_message()
        return redirect(self.get_success_url())


    
class ReservationImageDeleteView(CustomDeleteMixin, PermissionRequireMixin, View):
    permissions = [User.Roles.DOCTOR, User.Roles.ADMIN]
    model = ImageGallery
    success_url = reverse_lazy('clinic:reservation_list')
    success_message = 'تصویر با موفقیت حذف شد.'




class ReservationMedicineCreateView(CustomFormTemplateMixin, PermissionRequireMixin, CreateView):
    permissions = [User.Roles.DOCTOR, User.Roles.ADMIN]
    model = ReservationMedicine
    form_class = ReservationMedicineForm
    page_title = 'افزودن دارو جدید'

    def get_page_subtitle(self):
        return 'مراجعه کننده: ' + self.get_reservation().patient.get_full_name()
 
    def get_reservation(self):
        id = self.kwargs['pk']
        return Reservation.objects.get(id=id)

    def get_success_url(self):
        patient = self.object.reservation.patient
        return reverse('users:patient_details', kwargs={'pk': patient.id})

    def form_valid(self, form):
        obj = self.get_reservation()
        medicine = form.save(commit=False)
        medicine.reservation = obj
        medicine.save()
        return super().form_valid(form)
 

class IllnessListView(CustomListTemplateMixin, PermissionRequireMixin, ListView):
    model = Illness
    permissions = [User.Roles.DOCTOR, User.Roles.ADMIN]
    page_title = 'لیست بیماری ها'
    queryset = Illness.objects.all()
    context_object_name = 'illnesses'
    paginate_by = 100
    ordering = 'name'
    fields = ['name', 'description']
    header_buttons = [{'title': 'افزودن بیماری', 'url': reverse_lazy('clinic:new_illness')}]
    action_buttons = [
        {'title': 'ویرایش', 'url_name': 'clinic:update_illness', 'arg_field': 'id',
         'fa-icon': 'fa-edit', 'class': '', 'class_form_field': 'id'},
    ]


class IllnessCreateView(CustomFormTemplateMixin, PermissionRequireMixin, CreateView):
    permissions = [User.Roles.DOCTOR, User.Roles.ADMIN]
    model = Illness
    form_class = IllnessForm
    page_title = 'افزودن بیماری جدید'
    success_url = reverse_lazy('clinic:illness_list')
    cancel_url = reverse_lazy('clinic:illness_list')
    success_message = 'بیماری جدید با موفقیت ثبت شد.'



class IllnessUpdateView(IllnessCreateView, UpdateView):
    page_title = 'ویرایش بیماری'
    success_message = 'بیماری با موفقیت ویرایش شد.'


class ServiceListView(CustomListTemplateMixin, PermissionRequireMixin, ListView):
    model = Service
    permissions = [User.Roles.DOCTOR, User.Roles.ADMIN]
    page_title = 'لیست سرویس ها'
    queryset = Service.objects.all()
    context_object_name = 'services'
    paginate_by = 100
    ordering = 'name'
    fields = ['name', 'price', 'description']
    header_buttons = [{'title': 'افزودن سرویس', 'url': reverse_lazy('clinic:new_service')}]
    action_buttons = [
        {'title': 'ویرایش', 'url_name': 'clinic:update_service', 'arg_field': 'id',
         'fa-icon': 'fa-edit', 'class': '', 'class_form_field': 'id'},
    ]

    
class ServiceCreateView(CustomFormTemplateMixin, PermissionRequireMixin, CreateView):
    permissions = [User.Roles.DOCTOR, User.Roles.ADMIN]
    model = Service
    form_class = ServiceForm
    page_title = 'افزودن سرویس جدید'
    success_url = reverse_lazy('clinic:service_list')
    cancel_url = reverse_lazy('clinic:service_list')
    success_message = 'سرویس جدید با موفقیت ثبت شد.'
   
    
class ServiceUpdateView(ServiceCreateView, UpdateView):
    page_title = 'ویرایش سرویس'
    success_message = 'سرویس با موفقیت ویرایش شد.'
      

class BrandCompanyListView(CustomListTemplateMixin, PermissionRequireMixin, ListView):
    model = BrandCompany
    permissions = [User.Roles.DOCTOR, User.Roles.ADMIN]
    page_title = 'لیست شرکت های تولید کننده'
    queryset = BrandCompany.objects.all()
    context_object_name = 'brand_companies'
    paginate_by = 100
    ordering = 'name'
    fields = ['name', 'description']
    header_buttons = [{'title': 'افزودن شرکت', 'url': reverse_lazy('clinic:new_brand_company')}]
    action_buttons = [
        {'title': 'ویرایش', 'url_name': 'clinic:update_brand_company', 'arg_field': 'id',
         'fa-icon': 'fa-edit', 'class': '', 'class_form_field': 'id'},
    ]
    

class BrandCompanyCreateView(CustomFormTemplateMixin, PermissionRequireMixin, CreateView):
    permissions = [User.Roles.DOCTOR, User.Roles.ADMIN]
    model = BrandCompany
    form_class = BrandCompanyForm
    page_title = 'افزودن شرکت جدید'
    success_url = reverse_lazy('clinic:brand_company_list')
    cancel_url = reverse_lazy('clinic:brand_company_list')
    success_message = 'شرکت جدید با موفقیت ثبت شد.'
    
    
class BrandCompanyUpdateView(BrandCompanyCreateView, UpdateView):
    page_title = 'ویرایش شرکت'
    success_message = 'شرکت با موفقیت ویرایش شد.'

    
class BrandListView(CustomListTemplateMixin, PermissionRequireMixin, ListView):
    model = Brand
    permissions = [User.Roles.DOCTOR, User.Roles.ADMIN]
    page_title = 'لیست برند ها'
    queryset = Brand.objects.all()
    context_object_name = 'brands'
    paginate_by = 100
    ordering = 'name'
    fields = ['name', 'description']
    header_buttons = [{'title': 'افزودن برند', 'url': reverse_lazy('clinic:new_brand')}]
    action_buttons = [
        {'title': 'ویرایش', 'url_name': 'clinic:update_brand', 'arg_field': 'id',
         'fa-icon': 'fa-edit', 'class': '', 'class_form_field': 'id'},
    ]
    

class BrandCreateView(CustomFormTemplateMixin, PermissionRequireMixin, CreateView):
    permissions = [User.Roles.DOCTOR, User.Roles.ADMIN]
    model = Brand
    form_class = BrandForm
    page_title = 'افزودن برند جدید'
    success_url = reverse_lazy('clinic:brand_list')
    cancel_url = reverse_lazy('clinic:brand_list')
    success_message = 'برند جدید با موفقیت ثبت شد.'
    

class BrandUpdateView(BrandCreateView, UpdateView):
    page_title = 'ویرایش برند'
    success_message = 'برند با موفقیت ویرایش شد.'

    
class MedicineListView(CustomListTemplateMixin, PermissionRequireMixin, ListView):
    model = Medicine
    permissions = [User.Roles.DOCTOR, User.Roles.ADMIN]
    page_title = 'لیست دارو ها'
    queryset = Medicine.objects.all()
    context_object_name = 'medicines'
    paginate_by = 100
    ordering = 'name'
    fields = ['name', 'description']
    header_buttons = [{'title': 'افزودن دارو', 'url': reverse_lazy('clinic:new_medicine')}]
    action_buttons = [
        {'title': 'ویرایش', 'url_name': 'clinic:update_medicine', 'arg_field': 'id',
         'fa-icon': 'fa-edit', 'class': '', 'class_form_field': 'id'},
    ]
    
    
class MedicineCreateView(CustomFormTemplateMixin, PermissionRequireMixin, CreateView):
    permissions = [User.Roles.DOCTOR, User.Roles.ADMIN]
    model = Medicine
    form_class = MedicineForm
    page_title = 'افزودن دارو جدید'
    success_url = reverse_lazy('clinic:medicine_list')
    cancel_url = reverse_lazy('clinic:medicine_list')
    success_message = 'دارو جدید با موفقیت ثبت شد.'
    
    
class MedicineUpdateView(MedicineCreateView, UpdateView):
    page_title = 'ویرایش دارو'
    success_message = 'دارو با موفقیت ویرایش شد.'

   
    
    
    
    
