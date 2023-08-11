from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponseForbidden,JsonResponse
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



@login_required(login_url='signin')
def homepage(request):
    user_posts = Post.objects.all()
    profiles = Profile.objects.all()
    profile = get_object_or_404(Profile, user=request.user)
    for profile in profiles:
        profile.follower_count = Follower.objects.filter(following=profile).count()

    
    context = {

        'profile': profile,
        'user_posts' :  user_posts,
        'profiles':profiles,
        
    }
    return render(request,'index.html',context)

@login_required(login_url='signin')
def profile_view(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id)
    
    # Get the follower count for the profile
    follower_count = profile.following.count()  # Use the correct reverse relationship name
    
    context = {
        'profile': profile,
        'follower_count': follower_count,
    }
    return render(request, 'profile.html', context)

@login_required(login_url='signin')
def follower(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id)

    # Get or create the Follower instance for the current user
    follower, _ = Follower.objects.get_or_create(follower=request.user.profile)

    # Create a new relationship between the Follower and the Profile being followed
    if profile not in follower.following.all():
        follower.following.add(profile)
        messages.success(request, f'You are now following {profile.user.username}')
    else:
        follower.following.remove(profile)
        messages.success(request, f'You unfollowed {profile.user.username}')

    follower.save()

    return redirect('profile', profile_id=profile_id)




class settings_view(View):
    template_name = "setting.html"

    def get(self, request, *args, **kwargs):

        context = {

        }
        return render(request, self.template_name, context)
    
    
def sign_in(request):
    page = 'signin'
    # if request.user.is_authenticated:
    #     return redirect('home')
    
    if request.method == 'POST':
        email=request.POST['email']
        username=request.POST['username']
        password=request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request,"Invalid credentials")
        
        user = authenticate(request, username=username, password=password)


        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request,"Username and Password do no match!")
    context = {

    }
    return render(request,'signin.html',context)



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
            follower = Follower.objects.create(user=user, follower=profile)

            messages.success(request, 'Account created successfully. You can now sign in.')
            return redirect('signin')

    context = {}
    return render(request, 'signup.html', context)



def logoutuser(request):
    logout(request)
    return redirect('home')

def like(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if Like.objects.filter(user=request.user, liked_object=post).exists():
        like_to_delete = Like.objects.get(user=request.user, liked_object=post)
        like_to_delete.delete()
        post.like_count -= 1
        post.save()
    else:
        Like.objects.create(user=request.user, liked_object=post)
        post.like_count += 1
        post.save()

    return redirect('home')



    



    
