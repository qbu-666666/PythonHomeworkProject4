from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from blogs.views import register  # 新增导入

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # 认证相关
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/register/', register, name='register'),  # 新增注册路由
    
    path('', include('blogs.urls')),
]