from django.contrib import admin
from django.urls import path, include
import debug_toolbar
# from ..main import views
from django.contrib import admin

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("main.urls")),
    path("api/auth/", include("authentication.urls")),
    path("__debug__/", include(debug_toolbar.urls)),
    # path("peleza-backend-server/api/companies/", views.CompaniesList.as_view()),
]
