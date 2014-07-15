from django.shortcuts import render, get_object_or_404
from django.contrib.auth.forms import *
from datavis.models import Api

def serve(request, site):
    return render(request, site)

def login(request):
    form = AuthenticationForm()
    return render(request, 'authentication/login.html', {'form': form})
