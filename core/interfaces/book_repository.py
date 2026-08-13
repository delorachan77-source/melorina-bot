from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any

class IBookRepository(ABC):
    @abstractmethod
    def get_by_id(self, book_id: int) -> Optional[Dict[str, Any]]:
        pass
    
    @abstractmethod
    def get_all(self, page: int = 1, page_size: int = 20) -> List[Dict[str, Any]]:
        pass
    
    @abstractmethod
    def create(self, book_data: Dict[str, Any]) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def update(self, book_id: int, book_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        pass
    
    @abstractmethod
    def delete(self, book_id: int) -> bool:
        pass
    
    @abstractmethod
    def search(self, query: str) -> List[Dict[str, Any]]:
        pass
