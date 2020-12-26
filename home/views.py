from django.shortcuts import render, redirect
from django.http import HttpResponse
from home.models import Contact
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth  import authenticate,  login, logout
from blog.models import Post
# Create your views here.
def home(request):
    return render(request, 'home/home.html')

def contact(request):
    messages.success(request, 'Welcome to Contact Us.')
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone = request.POST['phone']
        issue = request.POST['issue']
        if len(phone)<12:
            messages.error(request, 'Kindly fill the phone number with country code. like +91XXXXXXXXXX')
        if len(first_name)==0 or len(last_name)==0 or len(email)==0 or len(phone)==0 or len(issue)==0:
            messages.error(request, 'None of the Field can be remain empty.')
        else:
            contact = Contact(first_name=first_name, last_name=last_name, email=email, phone=phone, content=issue)
            contact.save()
    return render(request, 'home/contact.html')

def about(request):
    return render(request, 'home/about.html')

def search(request):
    query=request.GET['query']
    if len(query)>78:
        allPosts=Post.objects.none()
    else:
        allPostsTitle= Post.objects.filter(title__icontains=query)
        allPostsAuthor= Post.objects.filter(author__icontains=query)
        allPostsContent =Post.objects.filter(content__icontains=query)
        allPosts=  allPostsTitle.union(allPostsContent, allPostsAuthor)
    if allPosts.count()==0:
        messages.warning(request, "No search results found. Please refine your query.")
    params={'allPosts': allPosts, 'query': query}
    return render(request, 'home/search.html', params)

def signup(request):
    return render(request, 'home/signup.html')

def loginL(request):
    return render(request, 'home/login.html')

def handleSignup(request):
    if request.method=="POST":
        # Get the post parameters
        name=request.POST['name']
        username=request.POST['username']
        email=request.POST['email']
        pass1=request.POST['password']
        pass2=request.POST['cnfpassword']

        # check for errorneous input
        if len(username)<10:
            messages.error(request, " Your user name must be under 10 characters")
            return redirect('home')

        if not username.isalnum():
            messages.error(request, " User name should only contain letters and numbers")
            return redirect('home')
        if (pass1!= pass2):
             messages.error(request, " Passwords do not match")
             return redirect('home')
        
        # Create the user
        myuser = User.objects.create_user(username, email, password)
        myuser.name = name
        myuser.save()
        messages.success(request, "Your account has been successfully created")
        return redirect('home')
    else:
        return HttpResponse("404 - Not found")

def handleLogin(request):
    if request.method=="POST":
        # Get the post parameters
        loginusername=request.POST['loginusername']
        loginpassword=request.POST['loginpassword']

        user=authenticate(username= loginusername, password= loginpassword)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect("home")
        else:
            messages.error(request, "Invalid credentials! Please try again")
            return redirect("home")

    return HttpResponse("404- Not found")

def handleLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('home')