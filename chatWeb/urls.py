from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from signup_app.views import signup,user_details
from login_app.views import user_login
from basic_app.views import index,logout_view
from chat_app.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index , name='index'),
    path('user_details/', user_details , name='user_details'),
    path('signup/', signup, name='signup'),
    path('login/', user_login, name='login'),
    path('logout/', logout_view, name='logout'),
    path('chat/start/', start_user_chat, name='start_user_chat'),
    path('chat/user/<int:room_id>/', user_chat, name='user_chat'),
    path('chat/group/new/', create_group_chat, name='create_group_chat'),
    path('chat/group/<int:room_id>/', group_chat, name='group_chat'),
    path('chat/delete/<int:room_id>/', delete_chat_room, name='delete_chat_room'),
    path('chat/group/delete/<int:room_id>/', delete_group_chat, name='delete_group_chat'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)