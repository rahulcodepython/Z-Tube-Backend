from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.TestIndex.as_view()),
    path("admin/", admin.site.urls),
    path("auth/", include("authentication.urls")),
    path("feed/", include("feed.urls")),
    path("ecom/", include("ecommerce.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
