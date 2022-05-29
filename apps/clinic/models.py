from datetime import datetime
from tabnanny import verbose
from django.db import models
from apps.core.models import AbstractModel


class Medicine(AbstractModel):
    name = models.CharField(max_length=100, verbose_name='نام دارو')
    description = models.TextField(null=True, blank=True, verbose_name='توضیحات')

    class Meta:
        verbose_name = 'دارو'
        verbose_name_plural = 'دارو'
        ordering = ('-id', )

    def __str__(self):
        return self.name

        
class Illness(AbstractModel):
    name = models.CharField(max_length=100, verbose_name='نام بیماری')
    description = models.TextField(null=True, blank=True, verbose_name='توضیحات')

    class Meta:
        verbose_name = 'بیماری'
        verbose_name_plural = 'بیماری'
        ordering = ('-id', )

    def __str__(self):
        return self.name

        
class Service(AbstractModel):
    name = models.CharField(max_length=100, verbose_name='نام خدمت')
    description = models.TextField(null=True, blank=True, verbose_name='توضیحات')
    price = models.IntegerField(verbose_name='قیمت (تومان)')

    class Meta:
        verbose_name = 'خدمت'
        verbose_name_plural = 'خدمت'
        ordering = ('-id', )
        
    def __str__(self):
        return self.name

    
class BrandCompany(AbstractModel):
    name = models.CharField(max_length=255, verbose_name='شرکت سازنده برند')

    class Meta:
        verbose_name = 'شرکت سازنده برند'
        verbose_name_plural = 'شرکت سازنده برند'
        
    def __str__(self):
        return self.name

class Brand(AbstractModel):
    company = models.ForeignKey(BrandCompany, related_name='brands', on_delete=models.PROTECT,
                                verbose_name='شرکت')
    name = models.CharField(max_length=255, verbose_name='نام برند')  

    class Meta:
        verbose_name = 'نام برند'
        verbose_name_plural = 'نام برند'
        
    def __str__(self):
        return f'{self.company.name} - {self.name}'


class BookTimeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def create_whole_date_times(self, date):
        books = []
        for time in self.model.TimesInDay.choices:
            books.append(self.model(date=date, time_in_day=time[0]))
        self.bulk_create(books)

    def create_today_times(self):
        today = datetime.today().date()
        self.create_whole_date_times(today)

    
class BookTime(AbstractModel):

    class TimesInDay(models.TextChoices):
        PM200 = '1400', '2:00 بعدازظهر'
        PM210 = '1410', '2:10 بعدازظهر'
        PM220 = '1420', '2:20 بعدازظهر'
        PM230 = '1430', '2:30 بعدازظهر'
        PM240 = '1440', '2:40 بعدازظهر'
        PM250 = '1450', '2:50 بعدازظهر'

        PM300 = '1500', '3:00 بعدازظهر'
        PM310 = '1510', '3:10 بعدازظهر'
        PM320 = '1520', '3:20 بعدازظهر'
        PM330 = '1530', '3:30 بعدازظهر'
        PM340 = '1540', '3:40 بعدازظهر'
        PM350 = '1550', '3:50 بعدازظهر'

        PM400 = '1600', '4:00 بعدازظهر'
        PM410 = '1610', '4:10 بعدازظهر'
        PM420 = '1620', '4:20 بعدازظهر'
        PM430 = '1630', '4:30 بعدازظهر'
        PM440 = '1640', '4:40 بعدازظهر'
        PM450 = '1650', '4:50 بعدازظهر'

        PM500 = '1700', '5:00 بعدازظهر'
        PM510 = '1710', '5:10 بعدازظهر'
        PM520 = '1720', '5:20 بعدازظهر'
        PM530 = '1730', '5:30 بعدازظهر'
        PM540 = '1740', '5:40 بعدازظهر'
        PM550 = '1750', '5:50 بعدازظهر'

        PM600 = '1800', '6:00 بعدازظهر'
        PM610 = '1810', '6:10 بعدازظهر'
        PM620 = '1820', '6:20 بعدازظهر'
        PM630 = '1830', '6:30 بعدازظهر'
        PM640 = '1840', '6:40 بعدازظهر'
        PM650 = '1850', '6:50 بعدازظهر'

        PM700 = '1900', '7:00 بعدازظهر'
        PM710 = '1910', '7:10 بعدازظهر'
        PM720 = '1920', '7:20 بعدازظهر'
        PM730 = '1930', '7:30 بعدازظهر'
        PM740 = '1940', '7:40 بعدازظهر'
        PM750 = '1950', '7:50 بعدازظهر'

        PM800 = '2000', '8:00 بعدازظهر'
        PM810 = '2010', '8:10 بعدازظهر'
        PM820 = '2020', '8:20 بعدازظهر'
        PM830 = '2030', '8:30 بعدازظهر'
        PM840 = '2040', '8:40 بعدازظهر'
        PM850 = '2050', '8:50 بعدازظهر'

        PM900 = '2100', '9:00 بعدازظهر'
        PM910 = '2110', '9:10 بعدازظهر'
        PM920 = '2120', '9:20 بعدازظهر'
        PM930 = '2130', '9:30 بعدازظهر'

    date = models.DateField(verbose_name='تاریخ', default=datetime.now)
    time_in_day = models.CharField(max_length=4, choices=TimesInDay.choices, verbose_name='ساعت')

    objects = BookTimeManager()

    class Meta:
        verbose_name = 'زمان رزرو'
        verbose_name_plural = 'زمان رزرو'
        ordering = ('-id', )
        unique_together = ('date', 'time_in_day')

    def __str__(self):
        return f"{self.date} {self.get_time_in_day_display()}"

        
class Reservation(AbstractModel):
    patient = models.ForeignKey('users.User', on_delete=models.PROTECT, verbose_name='بیمار',
                                related_name='reservations')
    staff = models.ForeignKey('users.User', on_delete=models.PROTECT, verbose_name='منشی',
                                related_name='created_reservations', null=True, blank=True)
    book_time = models.ForeignKey(BookTime, on_delete=models.PROTECT, verbose_name='زمان رزرو',
                                     related_name='reservations')
    visited_at = models.DateTimeField(verbose_name='تاریخ و ساعت مراجعه', null=True, blank=True)
    requested_services = models.ManyToManyField(Service, verbose_name='خدمات درخواستی',
                                              related_name='reservations')

    class Meta:
        verbose_name = 'رزرو'
        verbose_name_plural = 'رزرو'
        ordering = ('-id', )

    def __str__(self):
        return f"{self.patient} - {self.book_time}"


class ImageGallery(AbstractModel):

    class CaptureTimes(models.IntegerChoices):
        UNDEFINED = 0, 'نامشخص'
        BEFORE = 1, 'قبل از درمان'
        AFTER = 2, 'بعد از درمان'
        MEANTIME = 3, 'در مدت درمان'
        
    image = models.ImageField(verbose_name='تصویر', upload_to='gallery/')
    user = models.ForeignKey('users.User', verbose_name='کاربر', on_delete=models.PROTECT)
    description = models.TextField(null=True, blank=True, verbose_name='توضیحات')
    capture_time = models.IntegerField(choices=CaptureTimes.choices, default=CaptureTimes.UNDEFINED,
                                       verbose_name='زمان')
    reservation = models.ForeignKey(Reservation, verbose_name='رزرو', on_delete=models.PROTECT,
                                    null=True, blank=True)

    def __str__(self):
        time = self.get_capture_time_display()
        return f"{self.user} - {time}"

class ReservationService(AbstractModel):
    reservation = models.ForeignKey(Reservation, verbose_name='رزرو', on_delete=models.PROTECT,
                                    related_name='services')
    service = models.ForeignKey('clinic.Service', verbose_name='خدمت', on_delete=models.PROTECT,
                                related_name='reservation_services')
    service_brand = models.CharField(max_length=255, verbose_name='برند خدمت', null=True, blank=True)
    brand = models.ForeignKey(Brand, verbose_name='برند', on_delete=models.PROTECT,
                              related_name='reservations', null=True, blank=True)
    service_amount = models.CharField(max_length=100, verbose_name='میزان استفاده شده', null=True, blank=True)
    description = models.TextField(null=True, blank=True, verbose_name='توضیحات')
    final_price = models.DecimalField(max_digits=9, decimal_places=0, verbose_name='قیمت نهایی')

    class Meta:
        verbose_name = 'خدمت انجام شده'
        verbose_name_plural = 'خدمت انجام شده'

    def __str__(self):
        return f"{self.service.name} - {self.service_brand}"

    
class ReservationMedicine(AbstractModel):
    reservation = models.ForeignKey(Reservation, verbose_name='رزرو', on_delete=models.PROTECT,
                                    related_name='medicines')
    medicine = models.ForeignKey('clinic.Medicine', verbose_name='دارو', on_delete=models.PROTECT,
                                 related_name='reservations')
    how_to_use = models.TextField(verbose_name='نحوه استفاده', null=True, blank=True)

    class Meta:
        verbose_name = 'داروها'
        verbose_name_plural = 'داروها'

    def __str__(self):
        return f"{self.medicine.name}"

    