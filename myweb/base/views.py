from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Book, User, Genre, Author
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import MyUserCreationForm, BookForm, UserForm
from .seeder import seeder_func
from django.contrib import messages

# Create your views here.
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    seeder_func()
    books = Book.objects.filter(Q(name__icontains=q) | Q(description__icontains=q) | Q(author__name__icontains=q) | Q(genre__name__icontains=q))
    books = list(dict.fromkeys(books))
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
            messages.error(request, 'User does not exist!')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile', request.user.id)
        else:
            messages.error(request, 'User or Password is not correct!')

    return render(request, 'base/login.html')


def logout_user(request):
    logout(request)
    return redirect('home')

def register_user(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('profile', user.id)

        else:
            messages.error(request, 'Follow The Instructions and create proper user and password...')



    context = {'form': form}
    return render(request, 'base/register.html', context)

def add_book(request):
    authors = Author.objects.all()
    genres = Genre.objects.all()
    form = BookForm()

    if request.method == 'POST':
        book_author = request.POST.get('author')
        book_genre = request.POST.get('genre')

        author, created = Author.objects.get_or_create(name=book_author)
        genre, created = Genre.objects.get_or_create(name=book_genre)

        form = BookForm(request.POST)

        new_book = Book(picture=request.FILES['picture'], name=form.data['name'], author=author,
                        description=form.data['description'], file=request.FILES['file'], creator=request.user)
        print(Book.objects.filter(name=new_book.name))
        if not (Book.objects.filter(file=request.FILES['file']) or Book.objects.filter(name=new_book.name)):
            new_book.save()
            new_book.genre.add(genre)
        else:
            messages.error(request, 'File with same name already exists...')
        return redirect('home')

    context = {'form': form, 'authors': authors, 'genres': genres}
    return render(request, 'base/add_book.html', context)


def reading(request, id):
    book = Book.objects.get(id=id)
    return render(request, 'base/reading.html', {'book': book})


def delete_book(request, id):
    obj = Book.objects.get(id=id)

    if request.method == "POST":
        obj.picture.delete()
        obj.file.delete()
        obj.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': obj})


@login_required(login_url='login')
def update_user(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', user.id)

    context = {'form': form}
    return render(request, 'base/update_user.html', context)