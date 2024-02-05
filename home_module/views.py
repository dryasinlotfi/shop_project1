from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.


def index(request):
    return render(request, 'home_module/index_page.html')


def site_header_component(request):
    return render(request, 'shared/site_header_component.html')


def site_footer_component(request):
    return render(request, 'shared/site_footer_component.html')
