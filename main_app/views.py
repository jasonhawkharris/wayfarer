from django.shortcuts import render, redirect
from .models import City

# Create your views here.


def home(request):
    return render(request, 'base.html')

def cities(request):
    cities = City.objects.all()
    context = {'cities', cities}
    return render(request, 'cities.html', context)
