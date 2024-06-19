from django.shortcuts import render
from django.http import HttpResponse
from .models import Book, User

# Create your views here.
def home(request):
    books = Book.objects.all()
    context = {"books": books}
    return render(request, 'base/home.html', context)


def about(request):
    return render(request, 'base/about.html')


def profile(request, pk):
    user = User.objects.get(id=pk)
    books = user.books.all()
    context = {"books": books}
    return render(request, 'base/profile.html', context)