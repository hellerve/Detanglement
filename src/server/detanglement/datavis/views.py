from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from datavis.models import Api

def serve(request, site):
    if request.user.is_authenticated():
        return render(request, site)
    return redirect('accounts/login/')

def redir(request, site):
    return redirect(site)

def profile(request):
    if request.user.is_authenticated():
        if request.user.is_superuser:
            return redirect('/admin/')
        return render(request, 'datavis/index.html')
    raise PermissionDenied()