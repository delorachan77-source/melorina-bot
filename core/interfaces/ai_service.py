from abc import ABC, abstractmethod
from typing import Dict, Any

class IAIService(ABC):
    @abstractmethod
    async def summarize(self, text: str) -> str:
        pass
    
    @abstractmethod
    async def translate(self, text: str, target_lang: str) -> str:
        pass
    
    @abstractmethod
    async def chat(self, prompt: str) -> str:
        pass
    
    @abstractmethod
    async def analyze_book(self, book_text: str) -> Dict[str, Any]:
        pass
