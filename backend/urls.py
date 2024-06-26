from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from authentication.views import TestIndex

urlpatterns = [
    path("", TestIndex.as_view()),
    path("admin/", admin.site.urls),
    path("auth/", include("authentication.urls")),
    path("feed/", include("feed.urls")),
    path("ecom/", include("ecommerce.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
