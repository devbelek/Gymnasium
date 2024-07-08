from django.contrib import admin
from .models import UserProfile, Comment, CommentReply, Like


admin.site.register(UserProfile)
admin.site.register(Comment)
admin.site.register(CommentReply)
admin.site.register(Like)
