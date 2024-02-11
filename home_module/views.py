
from django.shortcuts import render
from todo.models import Todo
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view


def index(request):
    context = {
        'todos': Todo.objects.order_by('priority').all()
    }
    return render(request, 'home_module/index_page.html', context)


def site_header_component(request):
    return render(request, 'shared/site_header_component.html')


def site_footer_component(request):
    return render(request, 'shared/site_footer_component.html')


@api_view(['GET'])
def todos_json(request: Request):
    todos = list(Todo.objects.order_by('priority').all().values('title', 'is_done'))
    return Response({'todos': todos},status.HTTP_200_OK)


