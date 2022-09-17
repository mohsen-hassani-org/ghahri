import json
from .models import SmsHistory


class Kavenegar:
    def __init__(self, template, mobile, token1=None, token2=None, token3=None):
        self.template = template
        self.mobile = mobile
        self.token1 = token1
        self.token2 = token2
        self.token3 = token3
        self.response_code = None
        self.response_text = None

    def send_sms(self):        
        sms_history = SmsHistory.objects.create(
            template=self.template,
            mobile =self.mobile,
            token1 =self.token1,
            token2 =self.token2,
            token3 =self.token3
        )
        self.response_code, self.response_text = sms_history.send_request()
        sms_history.response_code = self.response_code
        sms_history.response_text = self.response_text
        sms_history.save()
