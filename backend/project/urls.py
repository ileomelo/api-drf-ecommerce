from django.contrib import admin
from django.urls import path
from rest_framework import routers
from core import views as core_views  # PARA SABER QUE VEM DO APP CORE

routers = routers.DefaultRouter()

urlpatterns = routers.urls 


urlpatterns += [
    path('admin/', admin.site.urls),
    path('contact/', core_views.ContactAPIView.as_view()),
]
