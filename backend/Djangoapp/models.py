from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.forms import ModelForm
from .models import * 
from django import forms 
from shortuuid.django_fields import ShortUUIDField
import shortuuid
from django.utils.text import slugify
from django_rest_passwordreset.signals import reset_password_token_created
from django.dispatch import receiver
from django.urls import reverse 
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags 
from django.db.models.signals import post_save
    
@receiver(reset_password_token_created)
def password_reset_token_created(reset_password_token,*args,**kwargs):
    sitelink="http://localhost:5173/"
    token="{}".format(reset_password_token.key)
    full_link = str(sitelink)+str("password-reset/")+str(token)
    
    print(token)
    print(full_link)

    context={
        'full_link': full_link,
        'email_address': reset_password_token.user.email
        
    }
    
    html_message = render_to_string("backend/email.html", context=context)
    plain_message = strip_tags(html_message)
    
    msg= EmailMultiAlternatives(
        subject="Request for resetting password for {title}".format(title=reset_password_token.user.email),
        body = plain_message,
        from_email ="sasshair.024@gmail.com",
        to=[reset_password_token.user.email]
    )

    msg.attach_alternative(html_message, "text/html")
    msg.send()
    
class CustomUserManager(BaseUserManager):
    def create_user(self,email,password=None, **extra_fields):
        if not email:
            raise ValueError('email is a required field')
        email = self.normalize_email(email)
        user=self.model(email=email,**extra_fields)
        user.set_password(password)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email,password=None, **extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        return self.create_user(email,password,**extra_fields)

class CustomUser(AbstractUser):
    email = models.EmailField(max_length=200, unique=True)
    # birthday = models.DateField(null=True,blank=True)
    username=models.CharField(max_length=200,null=True,blank=True)
    fullname = models.CharField(max_length= 100, null= True,blank=True)

    objects=CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
        mailusername, mobile = self.email.split("@")
        if self.fullname == "" or self.fullname == None:
            self.fullname = mailusername
        if self.username == "" or self.username == None:
            self.username = mailusername  
    
        super(CustomUser, self).save(*args, **kwargs)

class Profile (models.Model):
    user=models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    image =models.FileField(upload_to="image",default="profile/default-user.jpg",null=True,blank=True)
    fullname = models.CharField(max_length=100,null=True,blank=True)
    bio = models.CharField(max_length=100,null=True,blank=True)
    about = models.CharField(max_length=100,null=True,blank=True)
    author= models.BooleanField(default= False)
    country = models.CharField(max_length=100,null=True,blank=True)
    facebook = models.CharField(max_length=100,null=True,blank=True)
    instagram = models.CharField(max_length=100,null=True,blank=True)
    date=models.DateTimeField(auto_now_add=True)
    
        
    def __str__(self):
        return self.user.fullname
    
    
    def save_profile(self, *args, **kwargs):

        if self.fullname =="" or self.fullname is None:
            self.fullname = self.user.fullname
        super(Profile,self).save(*args, **kwargs)

def create_profile(sender, instance,created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
def save_profile(sender,instance, **kwargs):
    instance.profile.save()
    
post_save.connect(create_profile,sender=CustomUser)
post_save.connect(save_profile, sender= CustomUser)

class Topic(models.Model):
    title=models.CharField(max_length=100)
    picture=models.FileField(upload_to="image",null=True,blank=True)
    slug=models.SlugField(unique=True,null=True,blank=True)
    
    def __str__(self):
        return self.title
    
    # class Meta:
    #     ordering=["-date"]
    #     verboseName="Post"
        
    def save(self, *args, **kwargs):
        if self.slug=="" or self.slug == None:
            self.slug=slugify(self.title)
        super(Topic,self).save(*args, **kwargs)

    def post_count(self):
        return Post.objects.filter(topic=self).count()
    
class Post(models.Model):
    STATUS=(
        ("Active","Active"),
        ("Draft","Draft"),
        ("Disabled","Disabled"),
    )
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    profile=models.ForeignKey(Profile,on_delete=models.CASCADE, null= True,blank=True)
    picture=models.FileField(upload_to="image",null=True,blank=True)
    slug=models.SlugField(unique=True,null=True,blank=True)
    title=models.CharField(max_length=100)
    content =models.TextField(null=True,blank=True)
    topic=models.ForeignKey(Topic,on_delete=models.CASCADE,null=True,blank=True,related_name='posts')
    status=models.CharField(choices=STATUS,max_length=100,default="Active")
    view = models.IntegerField(default=0)
    likes=models.ManyToManyField(CustomUser,blank=True,related_name="likes")
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering=["-date"]
        verbose_name_plural="Post"
        
    def save(self, *args, **kwargs):
        if self.slug=="" or self.slug == None:
            self.slug=slugify(self.title) + "-" +shortuuid.uuid()[:2]
        super(Post,self).save(*args, **kwargs)

class Comment(models.Model):
    post=models.ForeignKey(Post,on_delete= models.CASCADE)
    email=models.CharField(max_length=100)
    fullname=models.CharField(max_length=100)
    content =models.TextField(null=True,blank=True)
    date = models.DateTimeField(auto_now_add=True)
    reply =models.TextField(null=True,blank=True)
    
    def __str__(self):
        return self.post.title
    
    class Meta:
        ordering=["-date"]
        verbose_name_plural="Comments"
        
class Bookmarks(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    feed = models.ForeignKey(Post,on_delete=models.CASCADE)
    date=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.feed.title
    
    class Meta:
        ordering=["-date"]
        verbose_name_plural="Bookmarks"

class Notif(models.Model):
    Type=(
        ("Likes","Likes"),
        ("Bookmarks","Bookmarks"),
        ("Comments","Comments"),
    )
    
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    feed = models.ForeignKey(Post,on_delete=models.CASCADE)
    date=models.DateTimeField(auto_now_add=True)
    type= models.CharField(choices=Type,max_length=100)
    
    def __str__(self):
        if self.feed:
            return f"{self.feed.title} - {self.type}"
    
    class Meta:
        ordering=["-date"]
        verbose_name_plural="Notif"

