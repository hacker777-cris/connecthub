from typing import Any
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from PIL import Image
from django.conf import settings
from django.utils import timezone

User = get_user_model()



class Profile(models.Model):
    relationship_choices = (
        ('single', 'single'),
        ('married', 'married'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(blank=False, max_length=100, default='user')
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(default='info@example.com')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    bio = models.TextField(default='about me')
    location = models.CharField(max_length=100, default='nairobi')
    work = models.CharField(max_length=200, default='unemployed')
    relationship_status = models.CharField(
        choices=relationship_choices,
        default='none',
        max_length=50
    )
    avatar = models.ImageField(
        default='avatar.jpg', 
        upload_to='profile_avatars' # dir to store the image
    )

    # Add a new field to store the follower count
    follower_count = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        # Calculate and update the follower count before saving the profile
        self.follower_count = self.followers.all().count()
        
        # save the profile
        super().save(*args, **kwargs)

        # resize the image
        img = Image.open(self.avatar.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.avatar.path)

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    caption = models.CharField(max_length=200)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, default=1)  # Replace '1' with the appropriate profile ID.
    post_image = models.ImageField(upload_to='profile_posts')
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    like_count = models.IntegerField(default=0)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.caption
    

class Follower(models.Model):
    follower = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='follower')
    following = models.ManyToManyField(Profile, related_name='following')
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=1)

    def __str__(self):
        return self.user.username

        


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, default=1)
    liked_object = models.ForeignKey('Post', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'liked_object')