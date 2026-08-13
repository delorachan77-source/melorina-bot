from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from core.services.book_service import BookService
from api.serializers.book_serializer import BookSerializer
from infrastructure.repositories.book_repository import DjangoBookRepository
from core.services.ai_service import GeminiService
from infrastructure.cache.redis_cache import RedisCache
import os

class BookListView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        repository = DjangoBookRepository()
        ai_service = GeminiService(os.getenv('GEMINI_API_KEY', ''))
        cache = RedisCache()
        self.book_service = BookService(repository, ai_service, cache)
    
    def get(self, request):
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 20))
        books = self.book_service.get_all_books(page, page_size)
        return Response({'success': True, 'data': books})


class BookCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        repository = DjangoBookRepository()
        ai_service = GeminiService(os.getenv('GEMINI_API_KEY', ''))
        cache = RedisCache()
        self.book_service = BookService(repository, ai_service, cache)
    
    def post(self, request):
        try:
            import asyncio
            book_data = request.data.copy()
            book_data['created_by_id'] = request.user.id
            
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            book = loop.run_until_complete(self.book_service.create_book(book_data))
            
            return Response({
                'success': True,
                'message': '✅ کتاب با موفقیت اضافه شد!',
                'data': book
            }, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({'success': False, 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class BookDetailView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        repository = DjangoBookRepository()
        ai_service = GeminiService(os.getenv('GEMINI_API_KEY', ''))
        cache = RedisCache()
        self.book_service = BookService(repository, ai_service, cache)
    
    def get(self, request, book_id):
        book = self.book_service.get_book(book_id)
        if not book:
            return Response({'success': False, 'error': 'کتاب پیدا نشد!'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'success': True, 'data': book})
    
    def delete(self, request, book_id):
        if not request.user.is_staff:
            return Response({'success': False, 'error': 'دسترسی ندارید!'}, status=status.HTTP_403_FORBIDDEN)
        
        result = self.book_service.delete_book(book_id)
        if not result:
            return Response({'success': False, 'error': 'کتاب پیدا نشد!'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'success': True, 'message': '✅ کتاب حذف شد!'})


class BookSearchView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        repository = DjangoBookRepository()
        ai_service = GeminiService(os.getenv('GEMINI_API_KEY', ''))
        cache = RedisCache()
        self.book_service = BookService(repository, ai_service, cache)
    
    def get(self, request):
        query = request.GET.get('q', '').strip()
        if not query:
            return Response({'success': False, 'error': 'عبارت جستجو را وارد کنید!'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            books = self.book_service.search_books(query)
            return Response({'success': True, 'data': books, 'count': len(books)})
        except ValueError as e:
            return Response({'success': False, 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
