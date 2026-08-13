from rest_framework import serializers
from core.models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            'id', 'title', 'author', 'description', 'summary',
            'genre', 'published_date', 'isbn', 'file', 'cover_image',
            'downloads', 'views', 'rating', 'is_free', 'price',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'downloads', 'views', 'rating', 'created_at', 'updated_at']
    
    def validate_file(self, value):
        if value.size > 50 * 1024 * 1024:
            raise serializers.ValidationError("حجم فایل نباید بیشتر از ۵۰ مگابایت باشد!")
        return value
