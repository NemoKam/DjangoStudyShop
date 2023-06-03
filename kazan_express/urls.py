from django.conf import settings
from django.conf.urls.static import static
from app.urls import urlpatterns as app_urlpatterns

urlpatterns = app_urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
