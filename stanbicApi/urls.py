from django.urls import path, include
import debug_toolbar

urlpatterns = [
    path("peleza-backend-server/api/", include("main.urls")),
    path("peleza-backend-server/api/auth/", include("authentication.urls")),
    path("peleza-backend-server/__debug__/", include(debug_toolbar.urls)),
]
