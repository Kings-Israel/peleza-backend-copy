from django.contrib import admin
from django.urls import path, include
import debug_toolbar
# from ..main import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("peleza-backend-server/admin/", admin.site.urls),
    path("peleza-backend-server/api/", include("main.urls")),
    path("peleza-backend-server/api/auth/", include("authentication.urls")),
    path("peleza-backend-server/__debug__/", include(debug_toolbar.urls)),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
