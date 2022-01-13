from django.shortcuts import render
from .models import Blog
from .forms import BlogForm
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse


def index(request):
    data = Blog.objects.all()
    return render(request, 'index.htm', context={'data': data})


def features(request):
    # data = Blog.objects.all()
    return render(request, 'blog/features.htm')


def index_gallery(request):
    data = Blog.objects.all()
    return render(request, 'blog/index-gallery.htm', context={'data': data})


def detail(request, post_id):
    post = Blog.objects.get(pk=post_id)
    return render(request, 'blog/detail.html', context={'post': post})


@login_required(login_url="login")
def add_post(request):
    form = BlogForm
    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = BlogForm()
    return render(request, 'blog/addpost.html', context={'form': form})


@login_required(login_url="login")
def edit_post(request, post_id):
    post = Blog.objects.get(pk=post_id)
    form = BlogForm(instance=post)

    if request.user != post.author:
        return HttpResponse("Siz buni o'zgartira olmaysiz")

    if request.method == "POST":
        form = BlogForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect("index")
    return render(request, "blog/editpost.html", {"form": form})


@login_required(login_url="login")
def delete_post(request, post_id):
    post = Blog.objects.get(pk=post_id)
    if request.user != post.author:
        return HttpResponse("Siz buni o'chira olmaysiz")
    else:
        post.delete()
        return redirect('index')


def search_post(request):
    query = request.GET.get('query')
    data = Blog.objects.filter(
        Q(title__icontains=query) |
        Q(text__icontains=query)
    )
    return render(request, 'blog/search.html', {'data': data})


def registerUser(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        form = UserCreationForm()
        if request.method == "POST":
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('login')

        return render(request, 'registration/signup.html', {'form': form})


def loginUser(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == "POST":
            name = request.POST.get('username')
            pwd = request.POST.get('password')
            user = authenticate(request, username=name, password=pwd)

            if user is not None:
                login(request, user)
                return redirect('index')
        return render(request, 'registration/login.html')


def logoutUser(request):
    logout(request)
    return redirect('login')
