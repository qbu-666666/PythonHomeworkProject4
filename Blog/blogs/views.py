from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.urls import reverse_lazy
from .models import BlogPost
from .forms import BlogPostForm

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

class HomePageView(ListView):
    model = BlogPost
    template_name = 'blogs/home.html'
    context_object_name = 'posts'

class NewPostView(LoginRequiredMixin, CreateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'blogs/new_post.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class EditPostView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'blogs/edit_post.html'
    success_url = reverse_lazy('home')

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user  # 只允许作者编辑

    def handle_no_permission(self):
        # 如果不是作者，返回 403 或重定向（这里重定向到首页）
        return redirect('home')