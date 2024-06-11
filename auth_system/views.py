from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate, login, logout
from .models import CustomUser


def register_user(request):
    if request.user.is_authenticated:
        return redirect("task-tracker:index")
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            name = request.POST.get('first_name')
            surname = request.POST.get('last_name')
            email = request.POST.get('email')
            password = request.POST.get('password')
            
            new_user = CustomUser.objects.create_user(username=username, first_name=name, last_name=surname, email=email ,password=password)
            new_user.save()
            user = authenticate(username=username, first_name=name, last_name=surname, email=email, password=password)
            login(request, user)

            return redirect("task-tracker:index")
        else:
            return render(request, "auth_system/register.html")

def login_user(request):
    if request.user.is_authenticated:
        return redirect("task-tracker:index")
    else:
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get('password')

            user = authenticate(username=username,password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, ("You have been succesfully logged in"))
                return redirect("task-tracker:index")
            else:
                messages.error(request, ("There was an error logging in, try again!"))
                return redirect("login")
            
        else:
            return render(request, "auth_system/login.html")


def logout_user(request):
    logout(request)
    messages.success(request, ("You were logged out"))
    return redirect("task-tracker:index")

def user_info(request, pk):
    if request.user.id == pk:
        try:
            user = CustomUser.objects.get(id=pk)
            context = {'user': user}
            return render(request, 'auth_system/user_info.html', context=context)
        except CustomUser.DoesNotExist:
            return HttpResponse (
                "User doesn't exist!",
                status=404
            )
    else:
        return HttpResponse ("Access denied", status=400)

def edit_user(request, user_id):
    if request.user.id == user_id:
        if request.method == 'POST':
            username = request.POST.get("username")
            name = request.POST.get('first_name')
            surname = request.POST.get('last_name')
            email = request.POST.get('email')
            phone_number = request.POST.get('phone_number')

            user = CustomUser.objects.get(id=user_id)
            user.username=username 
            user.email=email
            user.first_name=name
            user.last_name=surname
            user.phone_number=phone_number
            user.save()

            messages.success(request, "Profile info has been updated")
            return redirect(f"/user-info/{user_id}")
        else:
            return render(request, "auth_system/edit_user.html")
    else:
        return HttpResponse ("Access denied", status=400)

def change_password(request, user_id):
    if request.user.id == user_id:
        if request.method == 'POST':
            user = CustomUser.objects.get(id=user_id)
            password = request.POST.get('current_password')
            new_password = request.POST.get('new_password1')
            new_password2 = request.POST.get('new_password2')
            validated = check_password(password, user.password)
            if validated:
                if new_password == new_password2:
                    user.set_password(new_password)
                    user.save()
                    login(request, user)
                    messages.success(request, ("Password has been changed"))
                else:
                    messages.error(request, ("Passwords do not match"))
                    return redirect(f'/change-password/{user_id}')
            else:
                messages.error(request, ("Incorrect password"))
                return redirect(f'/change-password/{user_id}')
            return redirect(f"/user-info/{user_id}")
        else:
            return render(request, "auth_system/change_password.html")
    else:
        return HttpResponse ("Access denied", status=400)