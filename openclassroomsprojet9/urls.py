"""
URL configuration for openclassroomsprojet9 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path
from django.views.static import serve

from LiteReview import views

urlpatterns = [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}, name='media'),
    path('admin/', admin.site.urls),
    # path('login/', views.index),
    path('inscription/', views.inscription),
    path('logout/', views.logout),
    path('create_ticket/', views.create_ticket),
    path('dashboard/', views.dashboard),
    path('critique/', views.critique),
    path('<int:nid>/modifier_ticket/', views.modifier_ticket),
    path('followers/', views.followers),
    path('', views.index),
    path('addfollower/', views.add_follower),
    path('deletefollower',views.delete_follower)

]
