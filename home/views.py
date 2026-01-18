from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from .models import Author,Book,State,Profile
from django.core.paginator import Paginator
from rest_framework.views import APIView       #for customer profiles view
from .serializer import ProfileSerializer      #for customer profiles view
from rest_framework.response import Response   #for customer profiles view 


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

# only for pagination
def state_list(request):
    state_qs = State.objects.all()

    paginator = Paginator(state_qs, 3)  # 1 page = 2 books
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'states.html', {'page_obj': page_obj})

#custom profile views for pagination using restapi 
# http://127.0.0.1:8000/about/?page=1&item=3
class CustomeProfilesView(APIView):
    def get(self, request):
        profiles = Profile.objects.all()
        items = request.GET.get('item')
        paginator = Paginator(profiles, items)  # 1 page = 2 books
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        serializer = ProfileSerializer(page_obj, many=True)
        return Response(serializer.data)