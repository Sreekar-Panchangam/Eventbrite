from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.views.generic import CreateView
from . import forms

# Create your views here.
# Login and logout have been taken care in settings.py with redirect url

class Signup(CreateView):
    form_class = forms.CreateUserForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/signup.html'
