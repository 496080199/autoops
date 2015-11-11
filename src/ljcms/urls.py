"""ljcms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static  
from django.conf import settings

urlpatterns = [
    url(r'^$','info.views.server',name='server'),
    url(r'^add/$','info.views.server_add',name='server_add'),
    url(r'^edit/([0-9]+.[0-9]+.[0-9]+.[0-9]+)$','info.views.server_edit',name='server_edit'),
    url(r'^del/([0-9]+.[0-9]+.[0-9]+.[0-9]+)$','info.views.server_del',name='server_del'),
    url(r'^group/$','info.views.group',name='group'),
    url(r'^group_add/$','info.views.group_add',name='group_add'),
    url(r'^group_edit/([0-9]+)$','info.views.group_edit',name='group_edit'),
    url(r'^group_del/([0-9]+)$','info.views.group_del',name='group_del'),
    url(r'^hardware/$','info.views.hardware',name='hardware'),
    url(r'^software/$','info.views.software',name='software'),
    url(r'^configure/$','info.views.configure',name='configure'),
    url(r'^configure_upload/$','info.views.configure_upload',name='configure_upload'),
    url(r'^configure_del/([0-9]+)$','info.views.configure_del',name='configure_del'),
    url(r'^admin/', include(admin.site.urls)),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL , document_root = settings.MEDIA_ROOT) 

