from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from .yasg import urlpatterns as doc_urls
# from debug_toolbar.toolbar import debug_toolbar_urls

urlpatterns = ([
    path('accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls),
    path('api/', include('main.urls')),
    path('api/', include('secondary.urls')),
    path('api/', include('users.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
])
               # + debug_toolbar_urls()

urlpatterns += doc_urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns = [
    *i18n_patterns(*urlpatterns, prefix_default_language=False),
]