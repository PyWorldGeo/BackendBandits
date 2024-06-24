from django.shortcuts import render
from django.http import HttpResponse
from .models import Book, User, Genre
from django.db.models import Q


# Create your views here.
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    books = Book.objects.filter(Q(name__icontains=q) | Q(description__icontains=q) | Q(author__name__icontains=q) | Q(genre__name__icontains=q))
    books = list(set(books))
    # books = Book.objects.all()
    # print(books[2].users.all())
    heading = "Online Library"
    genres = Genre.objects.all()
    context = {"books": books, "heading": heading, 'genres': genres}
    return render(request, 'base/home.html', context)


def about(request):
    return render(request, 'base/about.html')


def profile(request, pk):
    user = User.objects.get(id=pk)
    # books = user.books.all()
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    books = user.books.filter(Q(name__icontains=q) | Q(description__icontains=q) | Q(author__name__icontains=q) | Q(genre__name__icontains=q))
    books = list(set(books))
    heading = "My Library"
    genres = Genre.objects.all()
    context = {"books": books, "heading": heading, 'genres': genres}
    return render(request, 'base/profile.html', context)