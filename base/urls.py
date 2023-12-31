from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from base.views import homepage,profile_view,follow_unfollow,create_post,sign_in,sign_up,logoutuser,like,profile_update,landingpage


urlpatterns = [
    path('',landingpage,name='landing'),
    path('home',homepage,name='home'),
    path('profile/<int:profile_id>/',profile_view,name='profile'),
    path('createpost',create_post,name='createpost'),
    path('signin', sign_in, name='signin'),
    path('signup', sign_up, name='signup'),
    path('logout',logoutuser,name='logout'),
    path('follow_unfollow/<int:profile_id>/',follow_unfollow , name='follow_unfollow'),
    path('like/<int:post_id>/',like,name='like_post'),
    path('profileupdate/<int:profile_id>/',profile_update,name='profileupdate'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)