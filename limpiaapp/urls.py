"""limpiaapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest.viewsets import loginAPI
from rest.viewsets import auxi_filter
from rest.viewsets import skills_filter
from rest.viewsets import agenda_filter
from rest.viewsets import consul_agend
from rest.viewsets import fecha_ViewSet
from rest.viewsets import consul_agendClien
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1.0/', include('rest.urls')),
    path('login', loginAPI.as_view(), name="prueba"),
    path('api/v1.0/auxi_filter/', auxi_filter.as_view()),
    path('api/v1.0/skills_filter/', skills_filter.as_view()),
    path('api/v1.0/agenda_filter/', agenda_filter.as_view()),
    path('api/v1.0/agend_full/', consul_agend.as_view()),
    path('api/v1.0/agend_clien/', consul_agendClien.as_view()),
    path('api/v1.0/fech_agend/', fecha_ViewSet.as_view())
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
