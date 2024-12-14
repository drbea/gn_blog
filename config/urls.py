
from django.contrib import admin
from django.urls import include, path

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path("authentication/", include("accounts.urls")),
    path("", include("home.urls")),
    path("message/", include("message.urls")),
    path("forum/", include("forum.urls")),
    path("dashboard/", include("dashboard.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
