from django.http import HttpResponse
from django.shortcuts import render

def landing_page(request):
    return HttpResponse("hello my name is Hari")

