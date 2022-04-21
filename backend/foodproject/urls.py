from django.contrib import admin
from django.db import router
from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     re_path(r'^api/', include('djoser.urls')),
#     re_path(r'^api/', include('djoser.urls.authtoken')),
#     path('api/', include('recipes.urls')),
#     path('api/', include('users.urls'))
# ]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('recipes.urls')),
    path('api/', include('users.urls'))
]
