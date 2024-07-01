from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Book, User, Genre
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

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

@login_required(login_url='login')
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


@login_required(login_url='login')
def adding(request, id):
    user = request.user
    book = Book.objects.get(id=id)
    user.books.add(book)
    return redirect('profile', user.id)


@login_required(login_url='login')
def delete(request, id):
    obj = Book.objects.get(id=id)

    if request.method == "POST":
        request.user.books.remove(obj)
        return redirect('profile', request.user.id)

    return render(request, 'base/delete.html', {'obj': obj})



def login_user(request):
    if request.user.is_authenticated:
        return redirect('profile', request.user.id)

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            pass

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile', request.user.id)
        else:
            pass

    return render(request, 'base/login.html')


def logout_user(request):
    logout(request)
    return redirect('home')
