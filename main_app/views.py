from django.shortcuts import render, redirect

# Create your views here.


def home(request):
    return render(request, 'base.html')

def cities(request):
    return render(request, 'cities.html')
