from django.shortcuts import render, get_object_or_404
from datavis.models import Api

def index(request):
    apis = Api.objects.filter()
    return render(request, 'datavis/index.html', {'apis': apis})

def apis(request):
    post = get_object_or_404(Api)
    return render(request, 'datavis/apis.html', {'apis': apis})

def visualize(request):
    return render(request, 'datavis/visualize.html')

def settings(request):
    return render(request, 'datavis/settings.html')
