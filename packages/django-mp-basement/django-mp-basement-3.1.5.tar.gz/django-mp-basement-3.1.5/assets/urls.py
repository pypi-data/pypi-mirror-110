
from django.conf import settings
from django.conf.urls.static import static


app_urls = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
