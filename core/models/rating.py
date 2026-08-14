from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class BookRating(models.Model):
    """
    مدل امتیاز و نظر کتاب
    این مدل برای ذخیره امتیازها و نظرات کاربران درباره کتاب‌ها استفاده میشه
    """
    
    user = models.ForeignKey(
        'User', 
        on_delete=models.CASCADE,
        related_name='ratings',
        verbose_name='کاربر'
    )
    
    book = models.ForeignKey(
        'Book', 
        on_delete=models.CASCADE,
        related_name='ratings',
        verbose_name='کتاب'
    )
    
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='امتیاز'
    )
    
    comment = models.TextField(
        blank=True,
        verbose_name='نظر'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاریخ ایجاد'
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='تاریخ بروزرسانی'
    )
    
    class Meta:
        db_table = 'book_ratings'
        unique_together = ('user', 'book')  # هر کاربر فقط یک بار به هر کتاب امتیاز میده
        indexes = [
            models.Index(fields=['book', '-created_at']),
            models.Index(fields=['user', 'book']),
        ]
        verbose_name = 'امتیاز کتاب'
        verbose_name_plural = 'امتیازهای کتاب'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.book.title}: {self.rating}⭐"
    
    @classmethod
    def get_average_rating(cls, book_id):
        """محاسبه میانگین امتیازات یک کتاب"""
        result = cls.objects.filter(book_id=book_id).aggregate(
            avg_rating=models.Avg('rating')
        )
        return round(result['avg_rating'] or 0, 1)
    
    @classmethod
    def get_rating_count(cls, book_id):
        """تعداد امتیازهای یک کتاب"""
        return cls.objects.filter(book_id=book_id).count()
