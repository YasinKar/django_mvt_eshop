from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from debug_toolbar.toolbar import debug_toolbar_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('site/', include('site_setting.urls')),
    path('shop/', include('shop.urls')),
    path('users/', include('users.urls')),
    path('cart/', include('cart.urls')),
    path('dashboard/', include('dashboard.urls'))
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + debug_toolbar_urls()