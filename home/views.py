from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from .models import Author,Book

def sign_up(request):
    if request.method=="POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        username = request.POST['username']
        password = request.POST['password']
        rpassword = request.POST['rpassword']
        email = request.POST['email']
        if User.objects.filter(username=username).exists():
            messages.success(request, 'User Already Exists')
            return redirect('/')
        elif User.objects.filter(email=email).exists():
            messages.success(request, 'Email Already Exists')
            return redirect('/')
        elif password!=rpassword:
            messages.success(request, 'password does not match confirm password')
            return redirect('/')
        else:
            user = User.objects.create_user(username=username,first_name=fname, last_name=lname,
            email=email,password=password)
            if user is not None:
                user.save()
                messages.success(request, 'User registered successfully!')
                return redirect('/')
            else:
                messages.success(request, 'required fields')
                return redirect('/')
    else:
        return render(request, 'signup.html')

def login_user(request):
    if request.method=="POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'User Logged In!')
            return redirect('/books')
        else:
            messages.success(request, 'username or password does not exists')
            return redirect('/')
    else:
        
        return render(request,'login.html')

def logout_user(request):
    logout(request)
    messages.success(request, 'User Loge Out!')
    return render(request,'login.html')

def books_detail(request):
    books = Book.objects.all()
    return render(request,'books.html',{'books': books})

