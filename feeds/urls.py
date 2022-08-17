from django.urls import path
from . import views


app_name = 'feeds'
urlpatterns = [
    path('', views.FeedView.as_view(), name='feeds-page'),
    path('<int:pk>/', views.FeedDetailView.as_view(), name='feed-detail-page'),
    path('update/<int:pk>/', views.UpdatePostView.as_view(), name='feed-update-page'),
    path('delete/<int:pk>/', views.DeletePostView.as_view(), name='feed-delete-page'),
    path('comment/update/<int:pk>/', views.CommentUpdateView.as_view(), name='update-comment-page'),
    path('comment/delete/<int:pk>/', views.CommentDeleteView.as_view(), name='delete-comment-page'),
    path('<int:pk>/like/', views.LikeFeedView.as_view(), name='like-feed'),
]