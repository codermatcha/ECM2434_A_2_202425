from django.contrib import admin
from django.urls import path, include
from django.conf import settings  # Import settings
import debug_toolbar  # Import Debug Toolbar for development

urlpatterns = [
    path("admin/", admin.site.urls),  # Admin panel
    path("", include("bingo.urls")),  # Include URLs from the bingo app
]

# ✅ Only include Debug Toolbar if DEBUG mode is enabled
if settings.DEBUG:
    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),  # Debug toolbar route
    ]
