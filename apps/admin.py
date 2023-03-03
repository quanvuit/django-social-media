from django.contrib import admin
from .models import Member, Post, Comment, Like, Friendship

# Register your models here.
@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ["user", "address", "avatar"]


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["member", "content", "image", "pub_date"]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["member", "content", "post"]



@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ["member", "post"]


@admin.register(Friendship)
class FriendshipAdmin(admin.ModelAdmin):
    list_display = ["member", "friend"]
