from django.urls import path
from api.views.book_views import (
    BookListView, BookCreateView, BookDetailView, BookSearchView
)

urlpatterns = [
    path('books/', BookListView.as_view(), name='book-list'),
    path('books/create/', BookCreateView.as_view(), name='book-create'),
    path('books/search/', BookSearchView.as_view(), name='book-search'),
    path('books/<int:book_id>/', BookDetailView.as_view(), name='book-detail'),
]
