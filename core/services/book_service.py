from typing import Optional, List, Dict, Any
from core.interfaces.book_repository import IBookRepository
from core.interfaces.ai_service import IAIService
from core.interfaces.cache import ICache
import json

class BookService:
    def __init__(
        self,
        repository: IBookRepository,
        ai_service: IAIService,
        cache: ICache
    ):
        self.repository = repository
        self.ai_service = ai_service
        self.cache = cache
    
    async def create_book(self, book_data: Dict[str, Any]) -> Dict[str, Any]:
        if not book_data.get('title'):
            raise ValueError("عنوان کتاب الزامی است!")
        
        if book_data.get('description'):
            summary = await self.ai_service.summarize(book_data['description'])
            book_data['summary'] = summary
        
        book = self.repository.create(book_data)
        self.cache.delete('books_popular')
        return book
    
    def get_book(self, book_id: int) -> Optional[Dict[str, Any]]:
        cache_key = f'book_{book_id}'
        cached_book = self.cache.get(cache_key)
        if cached_book:
            return json.loads(cached_book)
        
        book = self.repository.get_by_id(book_id)
        if book:
            self.cache.set(cache_key, json.dumps(book), ttl=3600)
        return book
    
    def get_all_books(self, page: int = 1, page_size: int = 20) -> List[Dict[str, Any]]:
        return self.repository.get_all(page, page_size)
    
    def search_books(self, query: str) -> List[Dict[str, Any]]:
        if len(query) < 2:
            raise ValueError("عبارت جستجو باید حداقل ۲ کاراکتر باشد!")
        return self.repository.search(query)
    
    def delete_book(self, book_id: int) -> bool:
        result = self.repository.delete(book_id)
        if result:
            self.cache.delete(f'book_{book_id}')
            self.cache.delete('books_popular')
        return result
