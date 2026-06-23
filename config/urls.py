from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls), # ✅ FIXED: Changed admin.site.admin_site.urls to admin.site.urls
    path('', include('core.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# --- Custom Admin Dashboard Branding ---
admin.site.site_header = "Shafnet Tours and Travel Administration"
admin.site.site_title = "Shafnet Tours and Travel Admin Portal"
admin.site.index_title = "Management Dashboard"