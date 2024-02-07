from rest_framework import serializers
from .models import OTPRequest


class RequestOTPSerializer(serializers.Serializer):
    receiver = serializers.CharField(max_length=50, allow_null=False)
    channel = serializers.ChoiceField(allow_null=False,choices=OTPRequest.OTPChannel)


class RequestOTPResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTPRequest
        fields = ['request_id']

class VerifyOtpRequestSerializer(serializers.Serializer):
    request_id = serializers.CharField(max_length=64, allow_null=False)
    password = serializers.CharField(max_length=64, allow_null=False)

class ObtainOtpSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=128, allow_null=False)
    refresh = serializers.CharField(max_length=128, allow_null=False)
    created = serializers.BooleanField()