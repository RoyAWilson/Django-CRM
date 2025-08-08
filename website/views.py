from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm


def home(request):
    # Check if logging in
    if request.method == "POST":
        user_name = request.POST['user_name']
        password = request.POST['password']
        # Authenticate User details:
        user=authenticate(request, username = user_name, password = password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have been logged in')
            return redirect('home')
        else:
            messages.success(request, 'There was an error logging in.  Please try again')
            return redirect('home')
    else:
        return render(request, 'home.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, 'You have now been logged out.')
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form=SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Authenticate and login:
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password = password)
            login(request, user)
            messages.success(request, message='You have successfully registered.  Welcome')
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form':form})