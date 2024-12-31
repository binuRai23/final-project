from django.contrib import admin 
from django.urls import path 
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import * 

router =DefaultRouter()
router.register('register', RegisterViewset, basename='register')
router.register('login', LoginViewset, basename='login')
# router.register('profile', ProfileViewset, basename='users')
# router.register('users', UserViewset, basename='users')
urlpatterns = [
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/<user_id>/', ProfileView.as_view(), name='profile'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # for topiclist
    path('topiclist/',TopicView.as_view(),name='topiclist'),
    path('topicposts/<topic_slug>/',PostTopicListView.as_view(),name='topicslug'),
    path('postlist/',PostListView.as_view(),name='postList'),
    path('postdetail/<slug>/',PostDetailView.as_view(),name='postdetail'),
    path('likes/',LikeView.as_view(),name='like'),
    path('comment/',CommentView.as_view(),name='comment'),
    path('bookmark/',BookmarkView.as_view(),name='bookmark'),
    # for dashboard
    path('blogdash/stats/<user_id>/',BlogDash.as_view(),name='blogdash'),
    path('postcreate/',CreatePost.as_view(),name='postcreate'),
    path('commentlist/<user_id>/',Comlist.as_view(),name='commentlist'),
    path('notifseen/',seenNotif.as_view(),name='seennotification'),
    path('notiflist/<user_id>/',DashNotiflist.as_view(),name='notificationlist'),
    path('commentreply/',CommentReply.as_view(),name='commentreply'),
    path('updatepost/<user_id>/<post_id>/',UpdatePost.as_view(),name='updatepost'),
    
]+ router.urls 
 
