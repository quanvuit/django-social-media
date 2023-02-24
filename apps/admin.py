from django.contrib import admin
from .models import Member, Post, Comment, Like, Friendship

# Register your models here.
admin.site.register(Member)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Friendship)
