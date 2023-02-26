from django.db import models
from django.contrib.auth.models import User


class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dob = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    avatar = models.ImageField(upload_to='profile_images', default='blank-profile-picture.png')

    def __str__(self):
        return self.user.username

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
