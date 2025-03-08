from typing import Any
from django.contrib.auth.models import User
from django.views.generic import DetailView, View, CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.urls import reverse
from posts.models import Post
from django.shortcuts import render
from followers.models import Followers
from .models import Profile
from nk_social_app.settings import logger

class ProfileDetailView( DetailView ):
    http_method_names = ["get"]
    template_name = "profiles/details.html"
    model = User
    context_object_name = "user"
    slug_field = "username"
    slug_url_kwarg = "username"
    
    def dispatch(self, request, *args, **kwargs) :
        self.request = request
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        user = self.get_object()
        context = super().get_context_data(**kwargs)
        context["total_posts"] = Post.objects.filter(author=user).count()
        context["total_followers"] = Followers.objects.filter(following__username=user.username).count()
        context["total_following"] = Followers.objects.filter(followed_by__username=user.username).count()
        if self.request.user.is_authenticated:
            context["check_follow"] = Followers.objects.filter(following=user, followed_by=self.request.user).exists()
        return context
    
class FollowView(LoginRequiredMixin, View):
    http_method_names = ["post"]
    
    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        
        if "username" not in data or "action" not in data:
            return HttpResponseBadRequest("Missing Data")
        
        try: 
            other_user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            return HttpResponseBadRequest("Missing User")
        
        if data['action'] == "Follow":
            #follow
            follower, created = Followers.objects.get_or_create(
                followed_by = request.user, #this is the logged in user
                following = other_user
            )
        else: 
            #unfollow
            try: 
                follower = Followers.objects.get(
                    followed_by = request.user,
                    following = other_user
                )
            except Followers.DoesNotExist:
                follower = None
                
            if follower: 
                follower.delete()
        
        follower_size = Followers.objects.filter(following__username=other_user).count()
        following_size = Followers.objects.filter(followed_by = other_user).count()
        
        return JsonResponse({
            "done": "Success",
            "wording": "Unfollow" if data["action"] == "Follow" else "Follow",
            "followers": follower_size,
            "following": following_size,
        }) 
        
        
class EditProfile(LoginRequiredMixin, TemplateView): 
    http_method_names = ["get","post"]
    template_name = "profiles/edit_profile.html"

    def post(self, request, *args, **kwargs):
        profile_image = request.FILES.get("image")
        cover_image = request.FILES.get("cover_image")
        username = request.POST.get("username")
        first_name =  request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
     

        # Validate images
        if profile_image: 
            if not self.verify_image(profile_image):
                return JsonResponse({
                    'error': 'Invalid profile image. Only JPEG, PNG, and GIF files are allowed.'
                }, status=400)
            request.user.profile.image = profile_image

        if cover_image:    
            if not self.verify_image(cover_image):
                return JsonResponse({
                    'error': 'Invalid backdrop image. Only JPEG, PNG, and GIF files are allowed.'
                }, status=400)
            request.user.profile.backdrop_image = cover_image
                 
        # Update user profile and user details
        if username:
            exist = User.objects.filter(username=username).exists()
            if not exist:
                request.user.username = username
            else: 
                return JsonResponse({
                    'error': "username already exist. Try Again"
                }, status=400)
        if first_name: 
            request.user.first_name = first_name
        
        if last_name:
            request.user.last_name = last_name
        
        if email:
            exist = User.objects.filter(email=email).exists()
            if not exist:
                request.user.email = email
            else: 
                return JsonResponse({
                    'error': "email already exist. Try Again"
                }, status=400)
        
        logger.info("saving user profile.........")
        # Save the changes to the user
        try:
            request.user.save()
        # Update or set profile images
            request.user.profile.save()
        except Exception as e:
            logger.error("Error saving user profile ", str(e))
        # Redirect to the user's profile page
        redirect_url = reverse('profiles:detail', kwargs={'username': request.user.username})
        response_data = {'redirect': redirect_url}
        return JsonResponse(response_data)
        

    @staticmethod
    def verify_image(image_file):
        allowed_types = ['image/jpeg', 'image/png', 'image/gif']

        # Check the content type of the image
        if image_file.content_type not in allowed_types:
            return False

        return True