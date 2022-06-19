from xml.etree.ElementInclude import include
from django.urls import path
from .views import (BookTimeCreateView, ClinicView, BookTimeListView,
                    QuickCreateReservationApiView, QuickCreatePatientApiView,
                    ReservationServiceCreateView, ReservationImageCreateView,
                    ReservationMedicineCreateView, ServiceListView,
                    BrandCompanyListView, BrandListView, MedicineListView,
                    IllnessListView, IllnessCreateView, IllnessUpdateView,
                    ServiceCreateView, ServiceUpdateView, BrandCompanyCreateView,
                    BrandCompanyUpdateView, BrandCreateView, BrandUpdateView,
                    MedicineCreateView, MedicineUpdateView, ReservationImageUpdateView,
                    ReservationImageDeleteView,
)

app_name = 'clinic'

view_urlpatterns = [
    path('_book_time_create/', BookTimeCreateView.as_view(), name='book_time_create'),
    path('', ClinicView.as_view(), name='clinic'),
    path('book-times/', BookTimeListView.as_view(), name='book_time_list'),
    path('reservation/<pk>/new-service/', ReservationServiceCreateView.as_view(), name='new_service'),
    path('reservation/<pk>/new-image/', ReservationImageCreateView.as_view(), name='new_image'),
    path('reservation/<pk>/update-image/', ReservationImageUpdateView.as_view(), name='update_image'),
    path('reservation/<pk>/update-image/', ReservationImageDeleteView.as_view(), name='delete_image'),
    path('reservation/<pk>/new-medicine/', ReservationMedicineCreateView.as_view(), name='new_medicine'),
    path('illnesses/', IllnessListView.as_view(), name='illness_list'),
    path('illnesses/new/', IllnessCreateView.as_view(), name='new_illness'),
    path('illnesses/<pk>/update/', IllnessUpdateView.as_view(), name='update_illness'),
    path('services/', ServiceListView.as_view(), name='service_list'),
    path('services/new/', ServiceCreateView.as_view(), name='new_service'),
    path('services/<pk>/update/', ServiceUpdateView.as_view(), name='update_service'),
    path('companies/', BrandCompanyListView.as_view(), name='brand_company_list'),
    path('companies/new/', BrandCompanyCreateView.as_view(), name='new_brand_company'),
    path('companies/<pk>/update/', BrandCompanyUpdateView.as_view(), name='update_brand_company'),
    path('brands/', BrandListView.as_view(), name='brand_list'),
    path('brands/new/', BrandCreateView.as_view(), name='new_brand'),
    path('brands/<pk>/update/', BrandUpdateView.as_view(), name='update_brand'),
    path('medicines/', MedicineListView.as_view(), name='medicine_list'),
    path('medicines/new/', MedicineCreateView.as_view(), name='new_medicine'),
    path('medicines/<pk>/update/', MedicineUpdateView.as_view(), name='update_medicine'),
]

api_urlpatterns = [
    path('api/user/create/', QuickCreatePatientApiView.as_view(), name='api_user_create'),
    path('api/reservation/create/', QuickCreateReservationApiView.as_view(), name='api_reservation_create'),
]

urlpatterns = view_urlpatterns + api_urlpatterns
