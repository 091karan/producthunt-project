from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from .models import Profile

def signup(request):
    if request.method == 'POST':
        # User has info and wants an account now!
        if request.POST['password1'] == request.POST['password2']:
            user = User.objects.filter(username=request.POST['username'])
            if user:
                print(user)
                return render(request, 'accounts/signup.html', {'error':'*Username has already been taken'})
            else:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'],first_name="karan")
                print(user)
                auth.login(request,user,backend='django.contrib.auth.backends.ModelBackend')
                return redirect('home')
        else:
            return render(request, 'accounts/signup.html', {'error':'*Passwords must match'})
    else:
        # User wants to enter info
        return render(request, 'accounts/signup.html')

def login(request):
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'],password=request.POST['password'])
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            return render(request, 'accounts/login.html',{'error':'*username or password is incorrect.'})
    else:
        return render(request, 'accounts/login.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('home')

def users(request,user_id):
    if request.method == 'POST':
        u = User.objects.get(pk=user_id)
        u.first_name = request.POST['first_name']
        u.last_name = request.POST['last_name']
        u.profile.birth_date = request.POST['birth_date']
        u.profile.photo = request.FILES['photo']
        u.profile.bio = request.POST['bio']
        u.profile.website = request.POST['website']
        u.profile.phone = request.POST['phone']
        u.profile.city = request.POST['city']
        u.profile.country = request.POST['country']
        u.save()
        return redirect('home')
    else:
        user = User.objects.get(id=user_id)
        return render(request,'accounts/users.html',{'user':user})
