from django.contrib import admin
from django.urls import path 
from . import views


urlpatterns = [
    
    path('', views.books, name="books"),
    path('addbook', views.addbook, name="addbook"),
    path('updatebook/<int:id>', views.updatebook, name="updatebook"),
    path('deletebook/<int:id>', views.deletebook, name="deletebook"),
    path('signup', views.signup, name="signup"),
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout")
    
    
    
]