from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from base.views import homepage,profile_view,follower,settings_view,sign_in,sign_up,logoutuser,like


urlpatterns = [
    path('',homepage,name='home'),
    path('profile/<int:profile_id>/',profile_view,name='profile'),
    path('settings',settings_view.as_view(),name='settings'),
    path('signin', sign_in, name='signin'),
    path('signup', sign_up, name='signup'),
    path('logout',logoutuser,name='logout'),
    path('follow/<int:profile_id>/',follower , name='follow'),
    path('like/<int:post_id>/',like,name='like_post'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)