from django.shortcuts import render
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .forms import Login_Form
# Create your views here.


def home(request):
    login_modal = Login_Form()
    context = {
        'login_form': login_modal
    }
    return render(request, 'base.html', context)
