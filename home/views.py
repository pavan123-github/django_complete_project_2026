from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from .models import Author,Book,State,Profile,SparePart,Vehical,Garment
from django.core.paginator import Paginator
from rest_framework.views import APIView       #for customer profiles view
from .serializer import ProfileSerializer,BookSerializer,SparePartSerializer,VehicalSerializer,GarmentSerializer   #for customer profiles view
from rest_framework.response import Response   #for customer profiles view 
from django.views import View  #for using class based view 
from rest_framework.decorators import action  #create custom method inside the class based view
from rest_framework.viewsets import ViewSet   #create custom method inside the class based view
from rest_framework import status
#celery 
from .tasks import delayed_task
from datetime import datetime


# function based view (FBV)
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

#simple function based view
def books_detail(request):
    books = Book.objects.all()
    return render(request,'books.html',{'books': books})

# only for pagination 
# http://127.0.0.1:8000/states test on browser
def state_list(request):
    state_qs = State.objects.all()

    paginator = Paginator(state_qs, 3)  # 1 page = 2 books
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'states.html', {'page_obj': page_obj})

#custom profile views for pagination using restapi 
# http://127.0.0.1:8000/profiles_detail/?page=1&item=3   
class CustomeProfilesView(APIView):
    def get(self, request):                 
        profiles = Profile.objects.all()
        items = request.GET.get('item')
        paginator = Paginator(profiles, items)  # 1 page = 2 books
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        serializer = ProfileSerializer(page_obj, many=True)
        return Response(serializer.data)                    #rendering json 
    
# class based view (CBV)
# http://localhost:8000/get_profile/1/  Test only browser
class MyView(View):
    def get(self,request, id):    #request ke bad id lene ka karan hai ki url me parameter ke sath bhejna
        profile = Profile.objects.filter(id=id)
        return render(request,'profiles.html',{'profile':profile})   #rendering html template

# http://localhost:8000/api/books/get_books/  Test on postman        
class BookViewSet(ViewSet):      # @action decorator does not work ApiView and View in argument of class 
    @action(detail=False, methods=['get'])  
    def get_books(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)     #rendering json 
    
#http://127.0.0.1:8000/api/books/2/get_single_book/
    @action(detail=True, methods=['get'])
    def get_single_book(self, request, pk=None):
        book = Book.objects.filter(id=pk).exists()
        if book is True:
            book_obj = book = Book.objects.get(id=pk)
            serializer = BookSerializer(book_obj)
            return Response(serializer.data)
        return JsonResponse({'msg':"id does not exists"})

# http://localhost:8000/api/books/create_book/
    @action(detail=False, methods=['post'])
    def create_book(self, request):
        serializer = BookSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
#custom crud apis without using Viewsets 
# ApIView me routers autometic maped hota hai get,post,put or delete methods se 
class SparePartListCreateApiView(APIView):
    def get(self, request):
        spare_part = SparePart.objects.all()
        serializer = SparePartSerializer(spare_part, many=True)
        return Response(serializer.data, status=200)
    
    def post(self, request):
        serializer = SparePartSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SparePartDetailAPIView(APIView):

    def get_object(self, id):
        try:
            return SparePart.objects.get(id=id)
        except SparePart.DoesNotExist:
            return None

    # READ single
    def get(self, request, id):
        spare_part = self.get_object(id)
        if not spare_part:
            return Response({'msg': 'Not Found'}, status=404)

        serializer = SparePartSerializer(spare_part)
        return Response(serializer.data)

    # UPDATE
    def put(self, request, id):
        spare_part = self.get_object(id)
        if not spare_part:
            return Response({'msg': 'Not Found'}, status=404)

        serializer = SparePartSerializer(spare_part, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    # DELETE
    def delete(self, request, id):
        spare_part = self.get_object(id)
        if not spare_part:
            return Response({'msg': 'Not Found'}, status=404)

        spare_part.delete()
        return Response({'msg': 'Deleted successfully'}, status=204)

#custom crud apis without using Viewsets class
# ViewSet me routers automatic maped nhi hota hai isliye costume method 
#bana sakte hai action decorator ka use karke
class VehicalViewSet(ViewSet):      # @action decorator does not work ApiView and View in argument of class 
    @action(detail=False, methods=['get'])  
    def get_vehicals(self, request):
        vehicals = Vehical.objects.all()
        serializer = VehicalSerializer(vehicals, many=True)
        return Response(serializer.data)     #rendering json
    
    
# celery background task calling
def run_task(request):
    print("TASK RUNNING AT:", datetime.now())
    return JsonResponse({'msg':'task runned'})


#class based api view
class GarmentsDetail(APIView):
    def get(self, request):
        garments = Garment.objects.all()
        serializer = GarmentSerializer(garments,many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = GarmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def put(self, request, pk, format=None):
        item = self.get_object(pk)
        serializer = GarmentSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE: Record delete karne ke liye
    def delete(self, request, pk, format=None):
        item = self.get_object(pk)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # Helper method for PUT/DELETE to get single object
    
    def get(self, request, pk):
        if pk:
            try:
                garment = Garment.objects.get(id=pk)
                serializer = GarmentSerializer(garment)
                return Response(serializer.data)
            except:
                return Response({'msg': 'Not Found'}, status=404)