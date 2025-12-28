from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import JsonResponse
from .models import BlogPost, Comment
from .forms import PostForm, CommentForm
from django.core.paginator import Paginator
from django.contrib.auth.models import User

class PostListView(ListView):
    model = BlogPost
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        return BlogPost.objects.order_by('-date_added')

class PostDetailView(DetailView):
    model = BlogPost
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'  # 添加这行，解决第一个问题

    def get_object(self):
        obj = super().get_object()
        obj.increase_views()  # 自动增加浏览量
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 修改这里：使用 post_comments 而不是 comments
        context['comments'] = self.object.post_comments.all().order_by('-created_date')
        context['comment_form'] = CommentForm()
        context['liked'] = self.object.likes.filter(id=self.request.user.id).exists() if self.request.user.is_authenticated else False
        context['total_likes'] = self.object.likes.count()
        return context

@login_required
def add_comment(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('blog:post_detail', pk=pk)
    return redirect('blog:post_detail', pk=pk)

@login_required
def like_post(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'liked': liked,
            'total_likes': post.likes.count()
        })
    return redirect('blog:post_detail', pk=pk)

class PostCreateView(LoginRequiredMixin, CreateView):
    model = BlogPost
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = BlogPost
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.owner

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = BlogPost
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:index')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.owner

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '注册成功！请登录。')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = user.blogpost_set.all()  # 这应该使用 owner 而不是 blogpost_set
    total_posts = posts.count()
    total_likes = sum(post.likes.count() for post in posts)
    # 修改这里：使用 post_comments 而不是 comments
    total_comments = sum(post.post_comments.count() for post in posts)
    
    # 添加总浏览量统计
    total_views = sum(post.views for post in posts)
    
    return render(request, 'blog/profile.html', {
        'profile_user': user,
        'posts': posts,
        'total_posts': total_posts,
        'total_likes': total_likes,
        'total_comments': total_comments,
        'total_views': total_views,  # 添加浏览量
    })