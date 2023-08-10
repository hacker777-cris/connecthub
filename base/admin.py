from django.contrib import admin
from base.models import Profile,Post,Like,Follower


admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Follower)
admin.site.register(Like)