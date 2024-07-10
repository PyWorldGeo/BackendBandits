from django.contrib.auth.forms import UserCreationForm
from .models import User, Book
from django.forms import ModelForm

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = '__all__'


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'username', 'email', 'bio', 'books']