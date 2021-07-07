from django.http import request
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post

# render is going to handle routing the render occuring in the HTML root.
# Create your views here.

def home(request):
        context = {
            'posts' : Post.objects.all()
        }
        return render(request,'blog/home.html',context)
        #this will call a template, search for a folder in our 
        # template folder named blog, and pull the home.html file 
        # from within that folder... I know...

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']   # this inverts the order by dates posted newest to oldest, default is oldest to newest.
    paginate_by = 5

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):  #these need to go before the view itself on the left, this has the mixin blocking people who are not logged in
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin, UpdateView):  #this has the mixin blocking people who are not logged in
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        elif self.request.user.is_superuser == True:
            return True
        return False    

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin, DeleteView):  #this has the mixin blocking people who are not logged in
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True 
        elif self.request.user.is_superuser == True:
            return True
        return False    

def about(request):
        context = {
            'posts' : Post.objects.all()
        }
        return render(request,'blog/about.html',context)
