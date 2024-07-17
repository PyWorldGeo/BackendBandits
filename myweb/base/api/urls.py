from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_routes),
    path('books/', views.get_books),
    path('books/<str:id>', views.get_book)
]