from django.http import HttpResponse
from django.shortcuts import render
from django.template.context_processors import request
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response

from rest_framework.views import APIView
from . import serialaizers

# Create your views here.

class OTPView(APIView):
    def get(self):
        serializer = serialaizers.RequestOTPSerializer(data=request.query_parms)
        if serializer.is_valid():
             pass
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

    def post(self):
        pass