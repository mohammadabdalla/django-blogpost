from django.shortcuts import render, redirect ,get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.list import ListView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Post
from .forms import CommentForm



# - Authentication models and functions
from . forms import CreateUserForm, LoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login, logout

class StartingPageView(ListView):
    
    template_name = "blog/index.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "posts"

    def get_queryset(self):
        queryset = super().get_queryset()
        data = queryset[:3]
        return data


class AllPostsView(LoginRequiredMixin,ListView):
    login_url = '/user-login/'
    template_name = "blog/all-posts.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "all_posts"


class SinglePostView(LoginRequiredMixin,View):
    login_url = '/user-login/'
    def is_stored_post(self, request, post_id):
        stored_posts = request.session.get("stored_posts")
        if stored_posts is not None:
          is_saved_for_later = post_id in stored_posts
        else:
          is_saved_for_later = False

        return is_saved_for_later

    def get(self, request, slug):
        post = Post.objects.get(slug=slug)
        
        context = {
            "post": post,
            "post_tags": post.tags.all(),
            "comment_form": CommentForm(),
            "comments": post.comments.all().order_by("-id"),
            "saved_for_later": self.is_stored_post(request, post.id)
        }
        return render(request, "blog/post-detail.html", context)

    def post(self, request, slug):
        comment_form = CommentForm(request.POST)
        post = Post.objects.get(slug=slug)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()

            return HttpResponseRedirect(reverse("post-detail-page", args=[slug]))

        context = {
            "post": post,
            "post_tags": post.tags.all(),
            "comment_form": comment_form,
            "comments": post.comments.all().order_by("-id"),
            "saved_for_later": self.is_stored_post(request, post.id)
        }
        return render(request, "blog/post-detail.html", context)


class ReadLaterView(LoginRequiredMixin,View):
    login_url = '/user-login/'
    def get(self, request):
        stored_posts = request.session.get("stored_posts")

        context = {}

        if stored_posts is None or len(stored_posts) == 0:
            context["posts"] = []
            context["has_posts"] = False
        else:
          posts = Post.objects.filter(id__in=stored_posts)
          context["posts"] = posts
          context["has_posts"] = True

        return render(request, "blog/stored-posts.html", context)


    def post(self, request):
        stored_posts = request.session.get("stored_posts")

        if stored_posts is None:
          stored_posts = []

        post_id = int(request.POST["post_id"])

        if post_id not in stored_posts:
          stored_posts.append(post_id)
        else:
          stored_posts.remove(post_id)

        request.session["stored_posts"] = stored_posts
        
        return HttpResponseRedirect("/")


############################################ auth views
# make the below code work
class AnonymousOnlyMixin():
    """
    A mixin that only allows anonymous users (users not logged in) to access the view.
    """
    def dispatch(self, request, *args, **kwargs):
        print("self.request.user.is_authenticated: ",self.request.user.is_authenticated)
        if self.request.user.is_authenticated:
            return HttpResponseRedirect("/")  # Redirect authenticated users to the home page or any other page
        return super().dispatch(request, *args, **kwargs)
        
class RegisterView(AnonymousOnlyMixin,View):
    def get(self, request):
      form = CreateUserForm()
      print("this isthe register form: ",form)
      context = {'registerform':form}
      return render(request, 'blog/register.html', context=context)
    
    def post(self, request):
       form = CreateUserForm(request.POST)
       
       context = {'registerform':form}
       if form.is_valid():
          form.save()
          return HttpResponseRedirect("/user-login")
       return render(request, 'blog/register.html', context=context)


           
class LoginView(AnonymousOnlyMixin,View):
    def get(self, request):
      form = LoginForm()
      context = {'loginform':form}
      return render(request, 'blog/user-login.html', context=context)


    def post(self, request):
      form = LoginForm(data=request.POST)
      context = {'loginform':form}
      if form.is_valid():
            print("inside is valid form")
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            print("this is the user: ",user)
            if user is not None:
               auth.login(request, user)    
               return HttpResponseRedirect("/")
      return render(request, 'blog/user-login.html', context=context)
         
            
            
                   


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/')