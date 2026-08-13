from typing import Optional, List, Dict, Any
from django.core.paginator import Paginator
from django.db.models import Q
from core.models import Book
from core.interfaces.book_repository import IBookRepository

class DjangoBookRepository(IBookRepository):
    def _to_dict(self, book: Book) -> Dict[str, Any]:
        return {
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'description': book.description,
            'summary': book.summary,
            'genre': book.genre,
            'published_date': book.published_date,
            'isbn': book.isbn,
            'file_url': book.file.url if book.file else None,
            'cover_url': book.cover_image.url if book.cover_image else None,
            'downloads': book.downloads,
            'views': book.views,
            'rating': book.rating,
            'is_free': book.is_free,
            'price': float(book.price),
            'created_at': book.created_at.isoformat(),
        }
    
    def get_by_id(self, book_id: int) -> Optional[Dict[str, Any]]:
        try:
            return self._to_dict(Book.objects.get(id=book_id))
        except Book.DoesNotExist:
            return None
    
    def get_all(self, page: int = 1, page_size: int = 20) -> List[Dict[str, Any]]:
        books = Book.objects.all()
        paginator = Paginator(books, page_size)
        return [self._to_dict(b) for b in paginator.get_page(page)]
    
    def create(self, book_data: Dict[str, Any]) -> Dict[str, Any]:
        book = Book.objects.create(**book_data)
        return self._to_dict(book)
    
    def update(self, book_id: int, book_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        try:
            book = Book.objects.get(id=book_id)
            for key, value in book_data.items():
                setattr(book, key, value)
            book.save()
            return self._to_dict(book)
        except Book.DoesNotExist:
            return None
    
    def delete(self, book_id: int) -> bool:
        try:
            Book.objects.get(id=book_id).delete()
            return True
        except Book.DoesNotExist:
            return False
    
    def search(self, query: str) -> List[Dict[str, Any]]:
        books = Book.objects.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(description__icontains=query)
        )[:50]
        return [self._to_dict(b) for b in books]
