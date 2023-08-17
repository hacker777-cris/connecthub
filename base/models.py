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
        ("in a Relationship", "In A Relationship"),
        ('engaged','engaged'),
        ('married', 'married'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(blank=False, max_length=100)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    bio = models.TextField()
    location = models.CharField(max_length=100)
    work = models.CharField(max_length=200)
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
    # Call the super method to save the profile
        super().save(*args, **kwargs)

    # Resize the image after saving and use the URL-based file path
        if self.avatar:
            img = Image.open(self.avatar.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.avatar.path)

class Post(models.Model):
    caption = models.CharField(max_length=200)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts') # Replace '1' with the appropriate profile ID.
    post_image = models.ImageField(upload_to='profile_posts')
    post_video = models.FileField(upload_to='profile_videos', blank=True, null=True)
    is_video = models.BooleanField(default=False)  # Indicates whether the post is a video
    created_date = models.DateTimeField(default=timezone.now)
    like_count = models.IntegerField(default=0)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.caption
    

class Follower(models.Model):
    follower = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='following')

    def __str__(self):
        return f"{self.follower.user.username} is following {self.following.user.username}"

        

class Like(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    liked_object = models.ForeignKey('Post', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('profile', 'liked_object')



