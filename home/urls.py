
from django.urls import path,include
from .import views 
from home.views import CustomeProfilesView


urlpatterns = [
    path('', views.sign_up, name="index"),
    path('submit_page', views.sign_up, name='signup'),
    path('login_user', views.login_user, name='login_user'),
    path('logout', views.logout_user, name='logout'),
    path('books', views.books_detail, name='books_detail'),
    path('states', views.state_list, name='state_list'),
    path("about/", CustomeProfilesView.as_view()),
]



