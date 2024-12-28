from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import * 
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model 
User =get_user_model()

class LoginSerializer(serializers.Serializer):
    email= serializers.EmailField()
    password = serializers.CharField()
    
    def to_representation(self,instance):
        ret = super().to_representation(instance)
        ret.pop('password',None)
        return ret 

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        # Get the token from the parent class
        token = super().get_token(user)

        # Add custom claims to the token
        token['fullname'] = user.fullname
        token['email'] = user.email
        token['username'] = user.username

        return token
    
    
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =('id','fullname','email','password')
        extra_kwargs={'password':{'write_only':True}}
        
    def create(self,validated_data):
        user = User.objects.create_user(
            fullname =validated_data['fullname'],
            email=validated_data['email'],
        )
        
        mailusername , mobile=user.email.split("@")
        user.username = mailusername
        user.set_password(validated_data['password'])
        user.save()
        return user 
    
class UserSerial(serializers.ModelSerializer):
    class Meta:
        model = User
        fields="__all__"
        
class ProfileSerial(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields="__all__"

class TopicSerial(serializers.ModelSerializer):
    post_count = serializers.SerializerMethodField()
    def get_post_count(self,topic):
        return topic.posts.count()
    
    class Meta:
        model= Topic
        fields=["id","title","picture","slug","post_count"]

    

class ComSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super(ComSerializer,self).__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.method =="POST":
            self.Meta.depth = 0
        else:
            self.Meta.depth = 1
            
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super(PostSerializer,self).__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.method =="POST":
            self.Meta.depth = 0
        else:
            self.Meta.depth = 1

class MarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmarks
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super(MarkSerializer,self).__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.method =="POST":
            self.Meta.depth = 0
        else:
            self.Meta.depth = 1
            
class NotifSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notif
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super(NotifSerializer,self).__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.method =="POST":
            self.Meta.depth = 0
        else:
            self.Meta.depth = 1
            
class AuthorSerial(serializers.Serializer):
    views = serializers.IntegerField(default=0)
    posts = serializers.IntegerField(default=0)
    likes = serializers.IntegerField(default=0)
    bookmarks = serializers.IntegerField(default=0)
    
