from datetime import datetime
from django.shortcuts import redirect, render
from django.views.generic import View
from .models import Reservation, BookTime


class BookTimeCreateView(View):
    def get(self, request, *args, **kwargs):
        date = request.GET.get('date')
        try:
            date = datetime.strptime(date, '%Y-%m-%d')
        except (ValueError, TypeError):
            date = datetime.now().today() 
        BookTime.objects.create_whole_date_times(date)
        return redirect('admin:clinic_booktime_changelist')
