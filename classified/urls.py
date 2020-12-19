"""classified URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include, re_path
from core import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name="index"),
    path('signup/', views.signup, name="signup"),
    path('signin/', views.signin, name="signin"),
    path('signout/', views.signout, name="signout"),
    path('classifieds/', views.classifieds, name="classifieds"),
    path('post/', views.post_classifieds, name="Post Classifieds"),
    path('dashboard/', views.dashboard, name="Dashboard"),
    path('myads/', views.my_ads, name="Dashboard My Ads"),
    path('backoffice/', admin.site.urls),
    path('summernote/', include('django_summernote.urls'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += [
    re_path(r'^classifieds/(?:city=(?P<locations>\w+)/)?/(?:category=(?P<category_id>\w+)/)?$', views.classifieds, name="classifieds")
]