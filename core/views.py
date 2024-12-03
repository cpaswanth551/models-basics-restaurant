from django.shortcuts import render

from django.contrib.contenttypes.models import ContentType

from core.models import Rating


def index(request):
    context = {}

    

    
    return render(request, "index.html", context)
