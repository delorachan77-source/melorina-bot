from django.db import models

class BookDownload(models.Model):
    """
    مدل تاریخچه دانلود کتاب
    این مدل برای ثبت هر بار دانلود کتاب توسط کاربران استفاده میشه
    """
    
    user = models.ForeignKey(
        'User', 
        on_delete=models.CASCADE,
        related_name='downloads',
        verbose_name='کاربر'
    )
    
    book = models.ForeignKey(
        'Book', 
        on_delete=models.CASCADE,
        related_name='downloads',
        verbose_name='کتاب'
    )
    
    downloaded_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='زمان دانلود'
    )
    
    ip_address = models.GenericIPAddressField(
        null=True, 
        blank=True,
        verbose_name='آدرس IP'
    )
    
    user_agent = models.CharField(
        max_length=500, 
        blank=True,
        verbose_name='مرورگر/دستگاه'
    )
    
    class Meta:
        db_table = 'book_downloads'
        unique_together = ('user', 'book')  # هر کاربر فقط یک بار هر کتاب رو دانلود میکنه
        indexes = [
            models.Index(fields=['user', 'book']),
            models.Index(fields=['-downloaded_at']),
        ]
        verbose_name = 'دانلود کتاب'
        verbose_name_plural = 'دانلودهای کتاب'
        ordering = ['-downloaded_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.book.title} ({self.downloaded_at})"
