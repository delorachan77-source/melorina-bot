from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# ========================================
# ===== تنظیمات Swagger (مستندسازی API) =====
# ========================================
schema_view = get_schema_view(
    openapi.Info(
        title="Melorina Bot API",
        default_version='v1',
        description="API مدیریت کتاب‌ها با قابلیت‌های هوش مصنوعی",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="melorina@example.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# ========================================
# ===== مسیرهای اصلی =====
# ========================================
urlpatterns = [
    # ===== پنل ادمین =====
    path('admin/', admin.site.urls),
    
    # ===== API =====
    path('api/v1/', include('api.urls')),
    
    # ===== مستندسازی Swagger =====
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

# ===== مسیرهای فایل‌های مدیا (در حالت DEBUG) =====
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
