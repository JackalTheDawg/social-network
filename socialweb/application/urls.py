from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as authViews
from application.chat import consumers

urlpatterns = [
    path('', page, name='session'),
    path('index/', page),
    path('id=<page_id>', profile_page),
    path('friends', friends_list, name='friends'),
    path('exit/', authViews.LogoutView.as_view(next_page='/'), name='exit'),
    path('gallery=<page_id>', photo_gallery, name='gallery'),
    path('video-gallery=<page_id>', video_gallery, name='video'),
    path('search', search_page, name='search'),
    path('chat-list=<page_id>', chat_list),
    path('chat=<chat_id>', chat_page, name='chat'),
    path('favorites', favorites),
    path('settings', page_settings),
    path('news', news)
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)