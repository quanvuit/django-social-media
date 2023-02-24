from django.db import models
from django.contrib.auth.models import User


class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dob = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    avatar = models.ImageField(upload_to='profile_images', default='blank-profile-picture.png')

    def __str__(self):
        return self.username

class Post(models.Model):
    content = models.TextField()
    image = models.ImageField(upload_to='post_images', blank=True, null=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(Member, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Comment(models.Model):
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(Member, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Like(models.Model):
    user = models.ForeignKey(Member, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.user.username

class Friendship(models.Model):
    user = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='user_member')
    friend = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='friend')

    def __str__(self):
        return self.user.username

# class Profile(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     id_user = models.IntegerField()
#     bio = models.TextField(blank=True)
#     profileimg = models.ImageField(upload_to='profile_images', default='blank-profile-picture.png')
#     location = models.CharField(max_length=256, blank=True)

#     def __str__(self):
#         return self.user.username

# class Post(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4)
#     user = models.CharField(max_length=256)
#     image = models.ImageField(upload_to='post_images')
#     caption = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     no_of_likes = models.IntegerField(default=0)

#     def __str__(self):
#         return self.user

# class LikePost(models.Model):
#     post_id = models.CharField(max_length=256)
#     username = models.CharField(max_length=256)

#     def __str__(self):
#         return self.username

# class FollowersCount(models.Model):
#     follower = models.CharField(max_length=256)
#     user = models.CharField(max_length=256)

#     def __str__(self):
#         return self.user 