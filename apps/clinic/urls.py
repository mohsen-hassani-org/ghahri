from django.urls import path
from .views import BookTimeCreateView

app_name = 'clinic'

urlpatterns = [
    path('_book_time_create/', BookTimeCreateView.as_view(), name='book_time_create'),
]
