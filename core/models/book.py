from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Book(models.Model):
    class Genre(models.TextChoices):
        FICTION = 'fiction', 'داستانی'
        NON_FICTION = 'non_fiction', 'غیرداستانی'
        POETRY = 'poetry', 'شعر'
        SCIENCE = 'science', 'علمی'
        HISTORY = 'history', 'تاریخی'
        ROMANCE = 'romance', 'عاشقانه'
        FANTASY = 'fantasy', 'فانتزی'
        MYSTERY = 'mystery', 'معمایی'
    
    title = models.CharField(max_length=255, db_index=True)
    author = models.CharField(max_length=255, db_index=True)
    description = models.TextField()
    summary = models.TextField(blank=True)
    genre = models.CharField(max_length=20, choices=Genre.choices)
    published_date = models.DateField()
    isbn = models.CharField(max_length=13, unique=True, null=True, blank=True)
    file = models.FileField(upload_to='books/%Y/%m/%d/')
    cover_image = models.ImageField(upload_to='book_covers/%Y/%m/%d/', null=True, blank=True)
    file_size = models.BigIntegerField(default=0)
    file_type = models.CharField(max_length=20, default='pdf')
    downloads = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0)
    rating_count = models.PositiveIntegerField(default=0)
    is_free = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, related_name='created_books')
    
    class Meta:
        db_table = 'books'
        ordering = ['-created_at']
