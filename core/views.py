from django.shortcuts import render

from .models import Comment, Rating, Restaurant



def index(request):
    context = {}

    return render(request, "index.html", context)
