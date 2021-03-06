import debug_toolbar
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.flatpages import views
from django.urls import include, path


urlpatterns = [
    path('auth/', include('apps.users.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('about/', views.flatpage, {"url": "/about/"}, name='about'),
    path('helper/', views.flatpage, {"url": "/helper/"}, name='helper'),
    path('tech/', views.flatpage, {"url": "/tech/"}, name='tech'),
    path('', include('apps.recipes.urls')),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += path('__debug__/', include(debug_toolbar.urls)),


handler404 = 'foodgram.views.page_not_found'  # noqa
handler500 = 'foodgram.views.server_error'  # noqa
