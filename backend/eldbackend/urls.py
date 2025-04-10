from django.contrib import admin
from django.urls import path, re_path
from django.views.generic import TemplateView, RedirectView
from django.conf import settings
from django.conf.urls.static import static
from .views import calculate_route

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/calculate/', calculate_route, name='calculate_route'),
    
    # Manifest and static file redirects
    path('manifest.json', RedirectView.as_view(url='/static/manifest.json')),
    path('favicon.ico', RedirectView.as_view(url='/static/favicon.ico')),
    path('logo192.png', RedirectView.as_view(url='/static/logo192.png')),
    
    # Catch-all for frontend routes (must be last)
    re_path(r'^.*$', TemplateView.as_view(template_name='index.html')),
]

# Serve static files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)