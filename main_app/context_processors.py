from .forms import Login_Form
from django.contrib.auth import login


def add_my_login_form(request):
    return {
        'login_form': Login_Form()
    }
