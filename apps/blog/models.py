from django.db import models
from apps.core.models import AbstractModel
from django.conf import settings

# Create your models here.

class BigSlider(AbstractModel):
    class TextPositions(models.TextChoices):
        LEFT = 'left', 'چپ'
        RIGHT = 'right', 'راست'
        CENTER = 'center', 'مرکز'

    title = models.CharField(max_length=255, verbose_name='عنوان')
    subtitle = models.CharField(max_length=255, verbose_name='زیر عنوان',
                                blank=True)
    body = models.TextField(verbose_name='متن', blank=True)
    image = models.ImageField(verbose_name='تصویر', upload_to='media/big_slider')
    button_text = models.CharField(max_length=255, verbose_name='متن دکمه',
                                   blank=True)
    button_link = models.CharField(max_length=255, verbose_name='لینک دکمه',
                                   blank=True)
    text_position = models.CharField(max_length=255, verbose_name='موقعیت متن',
                                     choices=TextPositions.choices,
                                     default=TextPositions.CENTER)
    page = models.CharField(max_length=255, verbose_name='صفحه', blank=True,
                            help_text='''اسلاگ صفحه‌ای که این المان در آن نمایش داده می‌شود.
                                         در صورتی که این فیلد خالی باشد،
                                         در صفحه‌ی اصلی نمایش داده می‌شود.''')
    is_publish = models.BooleanField(verbose_name='منتشر شود؟', default=False)

    class Meta:
        verbose_name = 'اسلایدر بزرگ'
        verbose_name_plural = 'اسلایدر بزرگ'
        ordering = ('-id',)

    def __str__(self):
        return self.title

    def get_image_url_or_default(self):
        if self.image:
            return self.image.url
        return settings.DEFAULT_BIG_SLIDER_URL 

    def image_tag(self):
        from django.utils.html import mark_safe
        return mark_safe(f'<img src="{self.image.url}" width="500px" />')
    image_tag.short_description = 'Image'

        
class Feature(AbstractModel):
    title = models.CharField(max_length=255, verbose_name='عنوان')
    subtitle = models.CharField(max_length=255, verbose_name='زیر عنوان', blank=True)
    thumbnail = models.ImageField(verbose_name='تصویر کوچک', upload_to='media/features')
    button_text = models.CharField(max_length=255, verbose_name='متن دکمه', blank=True)
    button_link = models.CharField(max_length=255, verbose_name='لینک دکمه', blank=True)
    page = models.CharField(max_length=255, verbose_name='صفحه', blank=True,
                            help_text='''اسلاگ صفحه‌ای که این المان در آن نمایش داده می‌شود.
                                         در صورتی که این فیلد خالی باشد،
                                         در صفحه‌ی اصلی نمایش داده می‌شود.''')
    is_publish = models.BooleanField(verbose_name='منتشر شود؟', default=False)
    
    class Meta:
        verbose_name = 'المان ویژگی'
        verbose_name_plural = 'المان ویژگی'
        ordering = ('-id',)

    def __str__(self):
        return self.title
    
    def get_thumbnail_url_or_default(self):
        if self.thumbnail:
            return self.thumbnail.url
        return settings.DEFAULT_THUMBNAIL_URL 
    
    def thumbnail_tag(self):
        from django.utils.html import mark_safe
        return mark_safe(f'<img src="{self.thumbnail.url}" width="200px" />')
    thumbnail_tag.short_description = 'Thumbnail'

