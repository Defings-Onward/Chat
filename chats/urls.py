from django.urls import path
from . import views

urlpatterns = [
    path('chats', views.chats, name='chats'),
    path('chat/def', views.default, name='def'),
    path('chat/<int:reciid>/<int:userid>/<int:name>/<int:is_user>', views.chat, name='chat'),
    path('calls', views.calls, name='calls'),
    path('chat/members/<int:groupId>', views.member, name='member'),
    path('chat/r_member/<int:groupId>', views.r_member, name='r_member'),
    path('media/<path:path>/', views.serve_media, name='serve_media'),
    path('chat/media/<int:mediaId>/', views.media, name='media'),
    path('chat/emoji', views.entertainment, name='entertainment')
]