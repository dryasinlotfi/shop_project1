from django.http import HttpResponse, HttpRequest, request
from django.shortcuts import render

from django.http import HttpResponse
from rest_framework import status,
request
from rest_framework.response import Response

from rest_framework.views import APIView
from . import serialaizers
from .models import OTPRequest


# Create your views here.

class OTPView(APIView):
    def get(self, request, *args, **kwargs):
        serializer = serialaizers.RequestOTPSerializer(data=request.query_parms)
        if serializer.is_valid():
             data = serializer.validated_data
             try:
                 otp = OTPRequest.objects.generate(data)
                 return Response(data=serialaizers.RequestOTPResponseSerializer(otp).data)
             except Exception as e:
                 return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data=serializer.errors)

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

    def post(self):
        serializer = serialaizers.VerifyOtpRequestSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            if OTPRequest.objects.is_valid(data['receiver'], data['request_id'], data['password']):
                pass
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
