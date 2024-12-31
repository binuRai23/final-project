from django.shortcuts import render
from rest_framework import viewsets, permissions
from .serializers import * 
from .models import * 
from django.db.models import Sum
from rest_framework.response import Response 
from django.contrib.auth import get_user_model, authenticate
from knox.models import AuthToken
from django.core.mail import send_mail
from rest_framework import generics
from rest_framework.decorators import api_view, APIView
User = get_user_model()
from rest_framework import status 
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class LoginViewset(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer

    def create(self, request):
        # Deserialize the incoming data
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            email=serializer.validated_data['email']
            password = serializer.validated_data['password']
            
            user=authenticate(request,email=email, password=password)
            
            if user:
                _,token= AuthToken.objects.create(user)
                return Response(
                    {
                        "user": self.serializer_class(user).data,
                        "token":token
                    }
                )
            else:
                return Response({"error":"Invalid Credentials"},status=401)
        else:
            return Response(serializer.errors,status=400)


class RegisterViewset(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=400)
       
        
class ProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ProfileSerial
    
    def get_object(self):
       user_id =self.kwargs['user_id']
       user = CustomUser.objects.get(id=user_id)
       profile=Profile.objects.get(user=user)
       
       return profile
    
    @classmethod
    def get_extra_actions(cls):
        return []

class TopicView(generics.ListAPIView):
    serializer_class=TopicSerial
    permission_classes=[permissions.AllowAny]
    
    def get_queryset(self):
        return Topic.objects.all()
    
class PostTopicListView(generics.ListAPIView):
    serializer_class= PostSerializer
    permission_classes=[permissions.AllowAny]
    
    def get_queryset(self):
         topic_slug= self.kwargs['topic_slug']  
         topic= Topic.objects.get(slug=topic_slug)
         posts = Post.objects.filter(topic=topic,status="Active")
        
         return posts

class PostListView(generics.ListAPIView):
    serializer_class= PostSerializer
    permission_classes=[permissions.AllowAny]
    
    def get_queryset(self):
        return Post.objects.filter(status="Active")

class PostDetailView(generics.RetrieveAPIView):
    serializer_class=PostSerializer
    permission_classes=[permissions.AllowAny]
    
    def get_object(self):
        slug= self.kwargs['slug']
        post = Post.objects.get(slug=slug,status="Active")
        post.view += 1 
        post.save()
        return post

class LikeView(APIView):
    def post(self,request):
        user_id = request.data.get('user_id') or input("Enter user_id: ")
        post_id = request.data.get('feed_id') or input("Enter post_id: ")

        user = CustomUser.objects.get(id=user_id)
        feed = Post.objects.get(id=post_id)
        
        if user in feed.likes.all():
            feed.likes.remove(user)
            return Response({"messsage":"Post Disliked"},status=status.HTTP_200_OK)
        else:
            feed.likes.add(user)
            
            Notif.objects.create(
                user=feed.user,
                feed=feed,
                type="Likes"
            )
            return Response({"message":"Post Liked"},status=status.HTTP_201_CREATED)

class CommentView(APIView):
    
    def post(self,request):
        post_id = request.data.get('post_id') or input("Enter post_id: ")
        fullname= request.data.get('fullname') or input("Enter fullname: ")
        email = request.data.get('email') or input("Enter email: ")
        content = request.data.get('content') or input("Enter comment: ")
    
        email = CustomUser.objects.get(email=email)
        post = Post.objects.get(id=post_id)
        
        Comment.objects.create(
            post=post,
            fullname= fullname,
            email=email,
            content=content
        )
        Notif.objects.create(
                user=post.user,
                feed=post,
                type="Comments"
            )
        return Response({"message":"comment sent"},status=status.HTTP_201_CREATED)

class BookmarkView(APIView):
    def post(self,request):
        user_id=request.data.get('user_id') or input ('Enter user_id:')
        post_id=request.data.get('post_id') or input ('Enter post_id')
        
        user=CustomUser.objects.get(id=user_id)
        post=Post.objects.get(id=post_id)
        mark = Bookmarks.objects.filter(feed=post, user=user).first()
        
        if mark:
            mark.delete()
            return Response({"message":"Bookmark unsaved"},status=status.HTTP_200_OK)
        else:
            Bookmarks.objects.create(
                user=user,
                feed=post,
            )
            Notif.objects.create(
                    user=post.user,
                    feed=post,
                    type="Bookmarks"
                )
            return Response({"message":"Bookmark saved"},status=status.HTTP_201_CREATED)

class BlogDash(generics.ListAPIView):
    serializer_class = AuthorSerial
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        user_id=self.kwargs['user_id']
        user= CustomUser.objects.get(id=user_id)
        
        views = Post.objects.filter(user=user).aggregate(view=Sum("view"))['view']
        posts = Post.objects.filter(user=user).count()
        likes = Post.objects.filter(user=user).aggregate(totalLikes=Sum("likes"))['totalLikes']
        bookmark= Bookmarks.objects.filter(feed__user=user).count()
        
        return[{
            "views":views,
            "posts":posts,
            "likes":likes,
            "bookmarks": bookmark,
        }]
    def list(self,request,*args, **kwargs):
        queryset= self.get_queryset()
        serializer = self.get_serializer(queryset,many=True)
        return Response(serializer.data)
    
class CreatePost(generics.CreateAPIView):
    serializer_class= PostSerializer
    permission_classes= [permissions.AllowAny]
    
    def create(self, request,*args, **kwargs):
        print(request.data)
        
        user_id = request.data.get("user_id")
        title = request.data.get("title")
        topic = request.data.get("topic")
        picture = request.data.get("picture")
        content = request.data.get("content")
        tags = request.data.get("tags")
        status = request.data.get("status")
        video = request.data.get("video")
    
        user= CustomUser.ibjects.get(id=user_id)
        topic = Topic.objects.get(id=topic)
        
        Post.objects.create(
            user=user,
            title=title,
            picture=picture,
            content=content,
            tags=tags,
            topic=topic,
            status=status,
            video= video
        )
        return Response({"message":"post created successfully!!"},status=status.HTTP_201_CREATED)
    
class DashPostlist(generics.ListAPIView):
        serializer_class= PostSerializer
        permission_classes=[permissions.AllowAny]
        
        def get_queryset(self):
           user_id=self.kwargs['use_id']
           user=CustomUser.User.objects.get(id=user_id)
           return Post.objects.filter(user=user).order_by("-id")
    
class Comlist(generics.ListAPIView):
        serializer_class=ComSerializer
        permission_classes=[permissions.AllowAny]
        
        def get_queryset(self):
            user_id=self.kwargs['user_id']
            user=CustomUser.objects.get(id=user_id)
           
            return Comment.objects.filter(post__user=user)
    
class DashNotiflist(generics.ListAPIView):
        serializer_class=NotifSerializer
        permission_classes=[permissions.AllowAny]
        
        def get_queryset(self):
            user_id=self.kwargs['user_id']
            user=CustomUser.objects.get(id=user_id)
           
            return Notif.objects.filter(seen=False,user=user)
    
class seenNotif(APIView):
        def post(self,request):
            notif_id = request.data['notif_id']
            notif= Notif.objects.get(id='notif_id')
            
            seen=True
            notif.save()
            
            return Response({"message":"notification marked as seen"},status=status.HTTP_200_OK)
        
class CommentReply(APIView):
        
        def post(self,request):
            com_id = request.data['com_id']
            reply = request.data['reply']
            
            comment=Comment.objects.get(id=com_id)
            comment.reply=reply
            
            comment.save()
            
            return Response({"message":"Comment response sent"},status=status.HTTP_201_CREATED)
        
class UpdatePost(generics.RetrieveUpdateDestroyAPIView):
    serializer_class=PostSerializer
    permission_classes=[permissions.AllowAny]
    
    def get_object(self):
        user_id = self.kwargs['user_id']
        user= CustomUser.objects.get(id=user_id)
        post_id=self.kwargs['post_id']
      
        return Post.objects.get(user=user,id=post_id)
    
    def update(self,request,*args, **kwargs):
        post_instance=self.get_object()
        
        title=request.data.get("title")
        picture = request.data.get("picture")
        topic= request.data.get("topic")
        content = request.data.get("content")
        tags = request.data.get("tags")
        status_value = request.data.get("status")
        video = request.data.get("video")
        
        topic = Topic.objects.get(id=topic)
        
        post_instance.title=title
        if picture != "undefined":
            post_instance.picture=picture
        post_instance.topic=topic
        post_instance.content=content
        post_instance.tags=tags        
        post_instance.status=status_value
        if video != "undefined":
            post_instance.video=video
        
        post_instance.save()
    
        return Response({"message": "post updated successfully"},status=status.HTTP_200_OK)
