from rest_framework import serializers
from apps.users.models import AuthSMSRequest


class AuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthSMSRequest
        fields = ('mobile', 'uuid')
        read_only_fields = ('uuid', )
