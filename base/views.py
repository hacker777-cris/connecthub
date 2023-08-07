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
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from base.forms import PostForm

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
        'profiles':profiles
    }
    return render(request,'index.html',context)


@login_required(login_url='signin')
def profile_view(request):
    profile = get_object_or_404(Profile, user=request.user)
    follower_count = Follower.objects.filter(following=profile).count()
    context = {

        'profile':profile,
        'follower_count':follower_count

    }
    return render(request,'profile.html', context)
    
@login_required(login_url='signin')
def follow_profile(request,profile_id):
    profile_to_follow = get_object_or_404(Profile, id=profile_id)
    follower,_ = Follower.objects.get_or_create(user=request.user)
    follower.following.add(profile_to_follow)

    return redirect('profile')

@login_required(login_url='signin')
def unfollow_profile(request, profile_id):
    profile_to_unfollow = Profile.objects.get(id=profile_id)
    follower = get_object_or_404(Follower, user=request.user)
    follower.following.remove(profile_to_unfollow)

    return redirect('profile')



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
            profile = Profile.objects.create(user=user)
            return redirect('signin')

    context = {}
    return render(request, 'signup.html', context)

def logoutuser(request):
    logout(request)
    return redirect('home')


# def like_object(request, object_id):
#     liked_object = get_object_or_404(Post, id=object_id)

#     # Check if the user has already liked the object
#     try:
#         Like.objects.get(user=request.user, liked_object=liked_object)
#         # If the Like already exists, it means the user has already liked the object
#         return JsonResponse({'message': 'You have already liked this object.'}, status=400)
#     except Like.DoesNotExist:
#         # If the Like doesn't exist, create a new Like instance with the user and the object
#         Like.objects.create(user=request.user, liked_object=liked_object)
#         return JsonResponse({'message': 'Object liked successfully.'}, status=200)




    
