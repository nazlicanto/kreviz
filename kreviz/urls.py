from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib.auth import views as auth_views
from kreviz import views

from chat.views import (chat_room_by_interest,
                        chat_room_by_room_name, priv_chat, bubble_chat)

from account.views import (register, view_profile)

from kreviz.views import (home, view_matches, index, about)

from matcher.views import (manage_interests, user_interests)



app_name = 'core'

urlpatterns = [
    # empty = root url
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('matcher/', include('matcher.urls')),
    path('manage_interests/', manage_interests, name='manage_interests'),
    path('login/', auth_views.LoginView.as_view(template_name='snippets/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='snippets/login.html'), name='logout'),
    path('matches/', view_matches, name='view-matches'),
    path('profile/<str:username>/', view_profile, name='view_profile'),
    path('', index, name='index'),
    path('about/', about, name='about'),
    path('chat/<str:interest_name>/', chat_room_by_interest, name='chat_room_by_interest'),
    path('chat/<str:room_name>/', chat_room_by_room_name, name='chat_room_by_room_name'),
    path('my-interests/', user_interests, name='user_interests'),
    path('priv/', priv_chat, name="priv_chat_list"),
    path('bubble/', bubble_chat, name='bubble_chat'),
    
]
"""
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

"""