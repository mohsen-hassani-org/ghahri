from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.generic import View
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from apps.core.permissions import PermissionRequireMixin
from apps.sms.exceptions import SendSMSException
from apps.users.models import AuthSMSRequest
from .serializers import AuthSerializer
from ..forms import PatientQuickForm, ReservationQuickForm
from ..models import WorkSample

User = get_user_model()


class QuickCreatePatientApiView(PermissionRequireMixin, View):
    permissions = [User.Roles.SECRETARY, User.Roles.DOCTOR, User.Roles.ADMIN]

    def post(self, request, *args, **kwargs):
        form = PatientQuickForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.staff = request.user
            patient.username = patient.mobile
            patient.save()
            return JsonResponse(status=200, data={'id': patient.id})
        return JsonResponse(status=400, data={'errors': form.errors})


class QuickCreateReservationApiView(PermissionRequireMixin, View):
    permissions = [User.Roles.SECRETARY, User.Roles.DOCTOR, User.Roles.ADMIN]

    def post(self, request, *args, **kwargs):
        form = ReservationQuickForm(request.POST)
        if form.is_valid():
            reservation = form.save()
            reservation.staff = request.user
            reservation.save()
            return JsonResponse(status=200, data={'id': reservation.id})
        return JsonResponse(status=400, data={'errors': form.errors})


class ConfirmMobileViewSet(GenericViewSet, CreateModelMixin):
    serializer_class = AuthSerializer
    queryset = AuthSMSRequest
    permission_classes = (AllowAny,)
    lookup_field = 'uuid'

    def perform_create(self, serializer):
        auth = serializer.save()
        auth.send_otp_code()

    @action(methods=['PATCH'], detail=True)
    def resend(self, request, uuid):
        auth = self._get_auth(uuid)
        if (timezone.now() - auth.updated_at).seconds < 60:
            return Response(data={'error': "برای ارسال مجدد کد یک دقیقه صبر کنید"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            auth.send_otp_code()
        except SendSMSException:
            return Response(data={"error": "خطایی در ارسال پیامک. لطفا با پشتیبان تماس بگیرید"},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)

    def _get_auth(self, uuid):
        return get_object_or_404(AuthSMSRequest, uuid=uuid)


class WorkSampleApiView(PermissionRequireMixin, APIView):
    permissions = [User.Roles.SECRETARY, User.Roles.DOCTOR, User.Roles.ADMIN, User.Roles.PATIENT]

    def get(self, request):
        work_sample = WorkSample.objects.filter(is_published=True).values_list()
        return Response(data={'model_to_reeturn':list(work_sample)}, status=status.HTTP_200_OK)
