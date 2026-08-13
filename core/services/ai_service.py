import aiohttp
from core.interfaces.ai_service import IAIService

class GeminiService(IAIService):
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    
    async def summarize(self, text: str) -> str:
        if len(text) < 50:
            return "متن کافی برای خلاصه‌سازی وجود ندارد!"
        prompt = f"خلاصه زیر رو به فارسی بنویس:\n\n{text[:5000]}"
        return await self._call_gemini(prompt)
    
    async def translate(self, text: str, target_lang: str = 'fa') -> str:
        prompt = f"متن زیر را به {target_lang} ترجمه کن:\n\n{text}"
        return await self._call_gemini(prompt)
    
    async def chat(self, prompt: str) -> str:
        return await self._call_gemini(prompt)
    
    async def analyze_book(self, book_text: str) -> dict:
        prompt = f"کتاب زیر را تحلیل کن:\n\n{book_text[:8000]}"
        result = await self._call_gemini(prompt)
        return {'analysis': result}
    
    async def _call_gemini(self, prompt: str) -> str:
        url = f"{self.base_url}?key={self.api_key}"
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload, timeout=30) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
                    return f"خطا: {response.status}"
        except Exception as e:
            return f"خطا: {str(e)[:100]}"
