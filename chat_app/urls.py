from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('base_user.urls')),
    path('chat/', include('core.urls')),
]
