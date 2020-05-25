from django.shortcuts import render, redirect
from .models import User
import bcrypt
from django.contrib import messages

def register(request):
    return render(request, 'register.html')

def registering(request):
    errors = User.objects.user_register_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    user_list_with_email = User.objects.filter(email=request.POST['email'])
    if user_list_with_email:
        messages.error(request, "That email is already registered!!")
        return redirect('/')
    pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
    User.objects.create(
        first_name = request.POST['first_name'],
        last_name = request.POST['last_name'],
        email = request.POST['email'],
        password = pw_hash,
    )
    user = User.objects.filter(email=request.POST['email'])
    if user:
        registered_user = user[0]
        request.session['userid'] = registered_user.id
    return redirect('/messages/wall')

def login(request):
    return render(request, 'login.html')

def logging(request):
    errors = User.objects.user_login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/home/login')
    user = User.objects.filter(email=request.POST['email'])
    if user:
        logged_user = user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['userid'] = logged_user.id
            return redirect('/messages/wall')
        else: 
            messages.error(request, "Your email and password do not match.")
    return redirect("/home/login")

