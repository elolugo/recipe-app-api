from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include('user.urls')),
    path('api/recipe/', include('recipe.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
"""
+ static() makes the media files available through accessing the media url.
Allowing us to see the media files without having to set up
a separate web server for serving these files.
Just accessing by 127.0.0.1:8000/MEDIA_URL we can see the media files.
The static files are served by default in Django,
so its not needed to add to urlpatterns.
"""
