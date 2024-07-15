from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here
class Author(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Book(models.Model):
    creator = models.ForeignKey('User', on_delete=models.SET("Unknown Creator"))
    picture = models.ImageField(null=True, blank=True)
    name = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.SET("Unknown Author"))
    genre = models.ManyToManyField(Genre, related_name='books', blank=True)
    description = models.TextField(max_length=500)
    file = models.FileField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name", 'created']

    def __str__(self):
        return f"{self.name} _ {self.author}"


class User(AbstractUser):
    books = models.ManyToManyField(Book, related_name='users', blank=True)
    avatar = models.ImageField(null=True, default='avatar.svg')
    bio = models.TextField(null=True)


class Comment(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.body
