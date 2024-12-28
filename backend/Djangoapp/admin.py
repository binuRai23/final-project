from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Topic)
admin.site.register(Comment)
admin.site.register(Bookmarks)
admin.site.register(Notif)