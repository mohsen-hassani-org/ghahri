import requests
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from apps.core.models import AbstractModel
from .exceptions import KavenegarResponseException


class SmsHistory(AbstractModel):
    class Meta:
        verbose_name = _('تاریخچه پیامکی')
        verbose_name_plural = _('تاریخچه پیامکی')

    mobile = models.CharField(max_length=20, verbose_name=_('شماره تلفن'))
    template = models.CharField(max_length=255, verbose_name='قالب')
    token1 = models.CharField(max_length=255, null=True, blank=True, verbose_name='توکن اول')
    token2 = models.CharField(max_length=255, null=True, blank=True, verbose_name='توکن دوم')
    token3 = models.CharField(max_length=255, null=True, blank=True, verbose_name='توکن سوم')
    staff = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('کارمند'), null=True)
    sent_at = models.DateTimeField(auto_now_add=True)
    response_text = models.CharField(max_length=100, null=True, blank=True, verbose_name=_('پاسخ درخواست'))
    response_code = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name=_('کد پاسخ درخواست'))

    def __str__(self):
        return self.mobile

    def send_request(self):
        api_key = settings.KAVENEGAR_API
        tokens = {}
        if self.token1:
            tokens['token'] = self.token1
        if self.token2:
            tokens['token2'] = self.token2
        if self.token3:
            tokens['token3'] = self.token3
        url = 'https://api.kavenegar.com/v1/{}/verify/lookup.json'.format(api_key)
        params = {'receptor': self.mobile, 'template': self.template, **tokens}
        res = requests.post(url, params=params)
        if res.status_code != 200:
            raise KavenegarResponseException
        data = res.json().get('return', {})
        return data.get('status'), data.get('message')

        
