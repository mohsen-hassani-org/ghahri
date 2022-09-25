from apps.sms.kavenegar.service import Kavenegar
from apps.sms.kavenegar.exceptions import KavenegarResponseException
from .exceptions import SendSMSException


class SMSInterface:
    @staticmethod
    def send_otp_code(auth_request):
        sms = Kavenegar(template='otpcode', mobile=auth_request.mobile, token1=auth_request.sms_code)
        try:
            sms.send_sms()
        except KavenegarResponseException as e:
            raise SendSMSException from e
        print(auth_request.sms_code)
        