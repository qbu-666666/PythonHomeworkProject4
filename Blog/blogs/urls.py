from django.urls import path
from .views import HomePageView, NewPostView, EditPostView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('new/', NewPostView.as_view(), name='new_post'),
    path('edit/<int:pk>/', EditPostView.as_view(), name='edit_post'),
]