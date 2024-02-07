from django.shortcuts import render
from rest_framework.request import Request
from rest_framework.response import Response
from .models import Todo
from .serializers import TodoSerializer
# Create your views here.


def all_todos(request: Request):
    todos = Todo.objects.order_by('priority').all()
    return Response()



