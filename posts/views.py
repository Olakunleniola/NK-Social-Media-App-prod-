from typing import Any
from django.views.generic import TemplateView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from .models import Post
from followers.models import Followers
from django.http import JsonResponse

# Create your views here.
class HopePage(LoginRequiredMixin, TemplateView) : 
    http_method_names = ["get"]
    template_name = "homepage.html"
    
    def dispatch (self, request, *args, **kwargs):
        self.request = request
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        
        if self.request.user.is_authenticated: 
            posts = Post.objects.all().order_by("-id")[0:30] 
            context["posts"] = posts
        
        return context
    
    
class FollowingView(LoginRequiredMixin, TemplateView):
    http_method_names = ["get"]
    template_name = "following.html"
    
    def dispatch (self, request, *args, **kwargs):
        self.request = request
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        
        if self.request.user.is_authenticated:
            follower = list(Followers.objects.filter(followed_by=self.request.user).values_list("following", flat=True))
            if follower:
                posts = Post.objects.filter(author__in=follower).order_by("-id")[0:60]
            else: 
                posts = Post.objects.filter(author=self.request.user).order_by("-id")[0:30]
            
            context["posts"] = posts
        return context
    
    
class PostDetailView(DetailView):
    http_method_names = ['get']
    template_name = "detail.html"
    model = Post
    context_object_name = 'post'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post"].text_shortened = context['post'].text[:14]
        return context
    
class CreateNewPost(LoginRequiredMixin, CreateView): 
    model = Post
    template_name = "create.html"
    fields = ['text']
    success_url= "/"
    
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        obj.save() 
        return super().form_valid(form)
    
    
    def post(self, request, *args, **kwargs):
        
        images = request.FILES.get("image"),
        
        for image in images:
        # Check if an image is provided
            if image:
                allowed_types = ['image/jpeg', 'image/png', 'image/gif']

                # Check the content type of the image
                if image.content_type not in allowed_types:
                    return JsonResponse({
                        'error': 'Invalid file format. Only image files (JPEG, PNG, GIF) are allowed.'
                    }, status=400)

        # Create a new Post with the image
        post = Post.objects.create(
            text=request.POST.get("post"),
            image=image,
            author=request.user,
        )
        
        return render(
            request,
            "includes/post.html",
            {
                "post": post,
                "show_link": True
            },
            content_type = "application/html"
        )