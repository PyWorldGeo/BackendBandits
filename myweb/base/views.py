from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def home(request):
    context = {"word": "Hello World!!!"}
    return render(request, 'home.html', context)


def about(request):
    return render(request, 'about.html')