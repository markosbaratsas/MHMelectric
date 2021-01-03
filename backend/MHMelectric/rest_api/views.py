from django.shortcuts import render
from django.http import HttpResponse
from rest_api.models import *

# Create your views here.
def index(request):
    return HttpResponse("<h1>We made it so far!</h1>")
    