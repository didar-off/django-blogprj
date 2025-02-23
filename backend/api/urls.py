from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from api import views as api_views

urlpatterns = [
    path('user/token/', api_views.MyTokenObtainPairView.as_view()),
    path('user/token/refresh/', TokenRefreshView.as_view()),
    path('user/register/', api_views.RegisterView.as_view()),
    path('user/profile/<user_id>/', api_views.ProfileView.as_view()),

    # Posts EndPoint
    path('post/category/list/', api_views.CategoryListAPIView.as_view()),
    path('post/category/post/<category_slug>/', api_views.PostCategoryListAPIView.as_view()),

    path('post/list/', api_views.PostListAPIView.as_view()),
    path('post/detail/<slug>/', api_views.PostDetailAPIView.as_view()),

    path('post/like-post/', api_views.LikePostAPIView.as_view()),
    path('post/comment-post/', api_views.PostCommentAPIView.as_view()),
    path('post/bookmark-post/', api_views.BookmarkAPIView.as_view()),

    path('author/dashboard/stats/<user_id>/', api_views.DashboardStats.as_view()),
    path('author/dashboard/comment-list/<user_id>/', api_views.DashboardCommentList.as_view()),
    path('author/dashboard/noti-list/<user_id>/', api_views.DashboardNotificationList.as_view()),
    path('author/dashboard/noti-mark-seen/', api_views.DashboardMarkNotificationAsSeen.as_view()),
    path('author/dashboard/reply-comment/', api_views.DashboardReplyCommentAPIView.as_view()),
    path('author/dashboard/post-create/', api_views.DashboardPostCreateAPIView.as_view()),
    path('author/dashboard/post-detail/<user_id>/', api_views.DashboardPostEditAPIView.as_view()),
]
