
from django.urls import path,include
from .import views 

urlpatterns = [
    path('', views.sign_up, name="index"),
    path('submit_page', views.sign_up, name='signup'),
    path('login_user', views.login_user, name='login_user'),
    path('logout', views.logout_user, name='logout'),
    path('books', views.books_detail, name='books_detail')
]


