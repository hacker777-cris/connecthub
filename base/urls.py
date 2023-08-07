from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from base.views import homepage,profile_view,follow_profile,unfollow_profile,settings_view,sign_in,sign_up,logoutuser


urlpatterns = [
    path('',homepage,name='home'),
    path('profile/', profile_view,name='profile'),
    path('settings',settings_view.as_view(),name='settings'),
    path('signin', sign_in, name='signin'),
    path('signup', sign_up, name='signup'),
    path('logout',logoutuser,name='logout'),
    path('follow<int:profile_id>/',follow_profile , name='follow'),
    path('unfollow<int:profile_id>/',unfollow_profile, name='unfollow'),
    # path('like/<int:object_id>/',like_object,name='like_object')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)