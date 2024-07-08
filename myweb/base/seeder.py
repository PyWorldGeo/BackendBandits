from .models import Author, Genre

def seeder_func():
    authors = ['Albert Kamiu', "Jacl London", 'Vaza Pshavela', 'Masanobu Fukuoka', "Alan Wots"]
    genres = ['Komedia', 'Drama', 'Melodrama', 'Horror', 'Historic']

    for author in authors:
        if not Author.objects.filter(name=author):
            new_author = Author(name=author)
            new_author.save()

    for genre in genres:
        if not Genre.objects.filter(name=genre):
            new_genre = Genre(name=genre)
            new_genre.save()