from multiprocessing import AuthenticationError
from django.forms import model_to_dict
from django.shortcuts import render, redirect, HttpResponse
from .models import Book
from django.contrib import messages 
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required


@login_required(login_url='/login')
def addbook(request):
    
    if request.method=="POST":
        title = request.POST.get('title')
        author = request.POST.get('author')
        rating = request.POST.get('rating')
        price = request.POST.get('price')
        thumbnail = request.POST.get('thumbnail')
        
        book = Book(title=title, author= author, rating=rating, price=price, thumbnail=thumbnail )
        book.save()
        return redirect("books")
        
    return render(request, "addbook.html")


def books(request):
    books = Book.objects.all()
    bookContext = {"books":books}
    return render(request, "books.html", bookContext)


@login_required(login_url='/login')
def updatebook(request, id):
    if request.method=="POST":
        title = request.POST.get('title')
        author = request.POST.get('author')
        rating = request.POST.get('rating')
        price = request.POST.get('price')
        thumbnail = request.POST.get('thumbnail')
        
        book = Book(id=id, title=title, author= author, rating=rating, price=price, thumbnail=thumbnail )
        book.save()
        return redirect("books")
    
    book = Book.objects.get(id=id)
    context = model_to_dict(book)    
    return render(request, "updatebook.html", context)

    
@login_required(login_url='/login')    
def deletebook(request, id):
    book = Book.objects.get(id=id)
    book.delete()
    return redirect("books")
    
      
      
def signup(request):
    if request.method=="POST":
        username=request.POST['username']
        email=request.POST['email']
        fname=request.POST['fname']
        lname=request.POST['lname']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']

        try:
            checkuser = User.objects.get(email=email)
        except User.DoesNotExist:
            checkuser = None
        if checkuser is not None:
            messages.warning(request, " Sorry, Email is Already Exist....!  ")
            return redirect("signup")
            
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name= fname
        myuser.last_name= lname
        myuser.is_staff = True
        myuser.save()
        messages.success(request, " Your Account has been Created successfully....! ")
        return redirect('/')
     
    return render(request, "signup.html")   
 

def login(request):
    if request.method=="POST":
        email = request.POST['email']
        pass1 = request.POST['pass']
        
        try:
            user1 = User.objects.get(email = email)
            if user1 is not None:
                user = authenticate(request, username = user1, password=pass1)
                if user is not None:
                    auth_login(request, user)
                    return redirect("/")
                else:
                    messages.warning(request, "Invalid Email Address OR Password...!  ")
                    return redirect("login")
        except User.DoesNotExist:
            messages.warning(request, "Invalid Email Address OR Password...!  ")
            return redirect("login")
            
    else:
        return render(request, "login.html")
    
    
@login_required(login_url='/login')            
def logout(request):
    auth_logout(request)
    messages.success(request, "User Logged Out successfully...!  ")
    return redirect("books")        
        
        