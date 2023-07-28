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

from LiteReview.views import inscription, signout, login, feed, follower, posts, review, ticket

urlpatterns = [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}, name='media'),
    path('admin/', admin.site.urls),
    # path('login/', views.index),
    path('inscription/', inscription.inscription),
    path('logout/', signout.logout),

    path('', login.index),
    path('index/', login.index),

    # suivi
    path('followers/', follower.followers),
    path('addfollower/', follower.add_follower),
    path('deletefollower/', follower.delete_follower),

    # flux
    path('feed/', feed.feed),

    # posts
    path('posts/', posts.user_posts),
    path('deletepost/', posts.delete_post),

    # critique
    path('critique/', review.critique),
    path('<int:nid>/edit_review/', review.edit_review),
    path('deletereview/', review.delete_review),

    # ticket
    path('<int:nid>/modifier_ticket/', ticket.modifier_ticket),
    path('create_ticket/', ticket.create_ticket),
    path('<int:nid>/reply_ticket/', ticket.reply_ticket)
]
