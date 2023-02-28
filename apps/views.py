from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User 
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import PostForm


from .models import Member, Post

@login_required(login_url='signin')
def index(request):
    return render(request, 'index.html')

@login_required(login_url='signin')
def create_post(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user.member
            post.save()
            messages.success(request, 'Bài đăng của bạn đã được tạo thành công!')
            return redirect('home')

    context = {'form': form}
    return render(request, 'create_post.html', context)

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
