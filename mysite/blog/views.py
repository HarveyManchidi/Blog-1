from logging import log
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from .models import *
from .forms import *
# Create your views here.


@login_required
def home(request):
    posts = Post.objects.all()

    context = {
        'posts': posts
    }
    return render(request, 'blog/home.html', context)


@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.save()
            return redirect(post.get_absolute_url())
    else:
        comment_form = CommentForm()
    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,

    }
    return render(request, 'blog/post_detail.html', context)


# ===================== CREATE POST ======================== #
@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            return redirect('blog-home')
    else:
        form = PostForm()
    context = {
        'form': form
    }
    return render(request, 'blog/create_post.html', context)


# ===================== UPDATE POST ======================== #
@login_required
def update_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user == post.author:
        if request.method == 'POST':
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                new_post = form.save(commit=False)
                new_post.author = request.user
                new_post.save()
                return redirect(post.get_absolute_url())
        else:
            form = PostForm(instance=post)
    else:
        return HttpResponse("not allowed")
    context = {
        'form': form,
    }
    return render(request, 'blog/update_post.html', context)


# ===================== DELETE POST ======================== #
@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user == post.author:
        if request.method == 'POST':
            post.delete()
            return redirect('blog-home')
        context = {
            'post': post,
        }
    else:
        return HttpResponse("not allowed")
    return render(request, 'blog/delete_post.html', context)

# ===================== LOGIN ============================ #
def signIn(request):
    if request.user.is_authenticated:
        return redirect('blog-home')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('blog-home')
        else:
            return HttpResponse("unaothorized")

    return render(request, 'blog/login.html')

# ===================== LOGOUT ============================ #
@login_required
def signout(request):
    logout(request)
    return redirect('blog-home')
