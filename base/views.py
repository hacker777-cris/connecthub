from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponseForbidden,JsonResponse,HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages 
from django.views import View
from base.models import Profile,Post,Like,Follower
from django.contrib.auth import login,logout
from django.views.generic import TemplateView
from django.views.generic import ListView, CreateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from base.forms import PostForm
from django.views.generic import View
from django.db.models import F
from base.forms import ProfileUpdateForm
from django.utils import timezone



@login_required(login_url='signin')
def homepage(request):
    logged_in_user_profile = Profile.objects.get(user=request.user)
    user_posts = Post.objects.all().order_by('-created_date')
    profiles = Profile.objects.exclude(user=request.user)
    logged_in_user_id = request.user.id
    profile = get_object_or_404(Profile, user=request.user)
    for profile in profiles:
        profile.follower_count = Follower.objects.filter(following=profile).count()

    
    context = {

        'profile': profile,
        'logged_in_user_id': logged_in_user_id,
        'logged_in_user_profile':logged_in_user_profile,
        'user_posts' :  user_posts,
        'profiles':profiles,
        
    }
    return render(request,'index.html',context)

@login_required(login_url='signin')
def profile_view(request, profile_id):
    
    profile = request.user.profile
    posts = profile.posts.all()
    
    # Get the follower count for the profile
    follower_count = profile.following.count()  # Use the correct reverse relationship name
    
    context = {

        'profile': profile,
        'posts':posts,
        'follower_count': follower_count,
    }
    

    return render(request, 'profile.html', context,)

@login_required(login_url='signin')
def profile_update(request, profile_id):
    profile = request.user.profile
    form = None

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('home')
        else:

            print(form.errors)
    else:
        form = ProfileUpdateForm(instance=profile)
    
    context = {
        'form': form
    }
        
    return render(request, 'settings.html', context)
@login_required(login_url='signin')
def create_post(request):
    if request.method == 'POST':
        caption = request.POST.get('caption')
        post_type = request.POST.get('post_type')
        post_file = request.FILES.get('post_file')

        post = Post(caption=caption, profile=request.user.profile, created_date=timezone.now())

        if post_type == 'image':
            post.post_image = post_file
            post.is_video = False
        elif post_type == 'video':
            post.post_video = post_file
            post.is_video = True

        post.save()

        return redirect('home')

    return render(request, 'createpost.html')




@login_required(login_url='signin')
def follow_unfollow(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id)
    if profile.user == request.user:
        return HttpResponseBadRequest("You cannot follow/unfollow yourself.")

    
    try:
        follower_obj = Follower.objects.get(follower=request.user.profile, following=profile)
        follower_obj.delete()
    except Follower.DoesNotExist:
        follower_obj = Follower(follower=request.user.profile, following=profile)
        follower_obj.save()

    return redirect('profile', profile_id=profile.id)





    template_name = "setting.html"

    def get(self, request, *args, **kwargs):

        context = {

        }
        return render(request, self.template_name, context)
    
def sign_in(request):
    page = 'signin'
    
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']

        # Try to authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to user's profile page
        else:
            messages.error(request, "Invalid username or password.")

    context = {}
    return render(request, 'signin.html', context)



def sign_up(request):
    page = 'signup'

    if request.method == 'POST':
        username = request.POST.get('username')
        firstname = request.POST.get('firstname', ' ')
        lastname = request.POST.get('lastname', ' ')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if not username:
            messages.error(request, 'Username is required')
        elif password1 != password2:
            messages.error(request, 'Passwords do not match')
        else:
            user = User.objects.create_user(username=username, password=password1, email=email, first_name=firstname, last_name=lastname)
            
            # Create the Profile instance
            profile = Profile.objects.create(user=user)
            
            # Create the corresponding Follower instance
            follower = Follower.objects.create(follower=profile, following=profile)

            messages.success(request, 'Account created successfully. You can now sign in.')
            login(request, user)
            return redirect('profileupdate', profile_id=user.profile.id)

    context = {}
    return render(request, 'signup.html', context)




def logoutuser(request):
    logout(request)
    return redirect('home')


def like(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # Get the profile of the current user
    profile = request.user.profile

    # Check if the user's profile has already liked the post
    existing_like = Like.objects.filter(profile=profile, liked_object=post).first()
    if existing_like:
        # User's profile has already liked, so unlike
        existing_like.delete()
        post.like_count -= 1
        post.save()  # Save the updated post instance
        messages.success(request, 'You unliked the post.')
    else:
        # User's profile has not liked, create a new Like
        like = Like.objects.create(profile=profile, liked_object=post)
        post.like_count += 1
        post.save()  # Save the updated post instance
        messages.success(request, 'You liked the post.')

    return redirect('home')







    



    

