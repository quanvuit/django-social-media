from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User 
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import PostForm, CommentForm, MemberForm

from django.db.models import Q
from .models import Member, Post, Like, Friendship

@login_required(login_url='signin')
def index(request):
    return render(request, 'index.html')

def search(request):
    query = request.GET.get('q')
    if query:
        results = Member.objects.filter(
            Q(user__username__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query)
        )
    else:
        results = None
    return render(request, 'search.html', {'results': results, 'query': query})

@login_required(login_url='signin')
def profile(request, username):
    member = get_object_or_404(Member, user__username=username)
    friends = member.friend.all()
    return render(request, 'profile.html', {'member': member, 'friends': friends})

@login_required(login_url='signin')
def add_friend(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    friend_id = request.POST.get('friend_id')
    if friend_id:
        friend = get_object_or_404(Member, id=friend_id)
        friendship, created = Friendship.objects.get_or_create(member=member, friend=friend)
        if not created:
            message = f"{friend.user.username} is already your friend."
            return render(request, 'profile.html', {'member': member, 'message': message})
        else:
            message = f"You are now friends with {friend.user.username}."
            return render(request, 'profile.html', {'member': member, 'message': message})
    else:
        message = "Please enter a valid friend ID."
        return render(request, 'profile.html', {'member': member, 'message': message})


@login_required(login_url='signin')
def like_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    user = request.user
    like_qs = Like.objects.filter(member=user.member, post=post)

    if like_qs.exists():
        like_qs.delete()
    else:
        Like.objects.create(member=user.member, post=post)

    return redirect('post_detail', post_id=post.id)

@login_required(login_url='signin')
def comment_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user.member
            comment.save()
            return redirect('/', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'index.html', {'form': form, 'post': post})

@login_required(login_url='signin')
def member_setting(request):
    member = request.user.member

    if request.method == 'POST':
        form = MemberForm(request.POST, request.FILES, instance=member)
        if form.is_valid():
            form.save()
            return redirect('/', username=request.user.username)
    else:
        form = MemberForm(instance=member)

    context = {
        'form': form,
        'member': member,
    }
    return render(request, 'setting.html', context)


@login_required(login_url='signin')
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.member = request.user.member
            post.save()
            # messages.success(request, 'Bài đăng của bạn đã được đăng thành công!')
            return redirect('/')
        else:
            # messages.success(request, 'Bài đăng của bạn đăng không thành công!')
            return redirect('/')

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Sai username hoặc password')
            return redirect('signin')
    else:
        return render(request, 'signin.html')
    
def signup(request):
    if request.method == 'POST':
        # Lấy thông tin từ form
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Kiểm tra xem tên đăng nhập hoặc email đã tồn tại chưa
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Tên đăng nhập đã tồn tại.')
            return redirect('signup')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email đã được sử dụng.')
            return redirect('signup')

        if password1 and password2 and password1 != password2:
            messages.error(request, 'Confirm password không chính xác')
            return redirect('signup') 
        # Tạo tài khoản User mới
        user = User.objects.create_user(username=username, email=email, password=password1)

        # Tạo tài khoản Member mới liên kết với User
        member = Member.objects.create(user=user)

        return redirect('signin')
    
    return render(request, 'signup.html')

@login_required(login_url='signin')
def logout_view(request):
    logout(request)
    return redirect('signin')
