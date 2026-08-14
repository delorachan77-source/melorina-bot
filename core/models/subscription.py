from django.db import models
from django.core.validators import MinValueValidator

class Subscription(models.Model):
    """
    مدل اشتراک کاربران
    این مدل برای مدیریت اشتراک‌های پریمیوم و طلایی استفاده میشه
    """
    
    class Plan(models.TextChoices):
        FREE = 'free', 'رایگان'
        PREMIUM = 'premium', 'پریمیوم'
        GOLD = 'gold', 'طلایی'
    
    user = models.ForeignKey(
        'User', 
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name='کاربر'
    )
    
    plan = models.CharField(
        max_length=20, 
        choices=Plan.choices,
        default=Plan.FREE,
        verbose_name='طرح اشتراک'
    )
    
    start_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاریخ شروع'
    )
    
    end_date = models.DateTimeField(
        verbose_name='تاریخ پایان'
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name='فعال'
    )
    
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='قیمت'
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
        db_table = 'subscriptions'
        indexes = [
            models.Index(fields=['user', '-end_date']),
            models.Index(fields=['plan', 'is_active']),
        ]
        verbose_name = 'اشتراک'
        verbose_name_plural = 'اشتراک‌ها'
        ordering = ['-created_at']
    
    def __str__(self):
        status = '✅ فعال' if self.is_active else '❌ غیرفعال'
        return f"{self.user.username} - {self.plan} ({status})"
    
    @classmethod
    def get_active_subscription(cls, user_id):
        """دریافت اشتراک فعال کاربر"""
        try:
            return cls.objects.get(
                user_id=user_id,
                is_active=True,
                end_date__gt=models.functions.Now()
            )
        except cls.DoesNotExist:
            return None
    
    @classmethod
    def create_subscription(cls, user_id, plan, days=30):
        """ایجاد اشتراک جدید برای کاربر"""
        from django.utils import timezone
        from datetime import timedelta
        
        # غیرفعال کردن اشتراک‌های قبلی
        cls.objects.filter(user_id=user_id, is_active=True).update(is_active=False)
        
        # ایجاد اشتراک جدید
        return cls.objects.create(
            user_id=user_id,
            plan=plan,
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=days),
            price=cls._get_plan_price(plan)
        )
    
    @classmethod
    def _get_plan_price(cls, plan):
        """دریافت قیمت هر طرح"""
        prices = {
            'free': 0,
            'premium': 50_000,
            'gold': 120_000,
        }
        return prices.get(plan, 0)
