from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record


def home(request):

    # Grab records from database (is it a great idea to grab them before user is logged in? How would this affect view permissions?)
    records = Record.objects.all()


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
        return render(request, 'home.html', {'records': records})

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
    return render(request, 'register.html', {'form':form})

def customer_record(request, pk):
    if request.user.is_authenticated:
        customer_record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'customer_record': customer_record})
    else:
        messages.success(request, message='You must be logged in to view that page')
        return redirect('home')

def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_it = Record.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "You have successfully deleted the record.")
        return redirect('home')
    else:
        messages.success(request, "You have to be logged in to delete a record.  Please login and try again.")
        return redirect('home')

def add_record(request):
        form = AddRecordForm(request.POST or None)
        if request.user.is_authenticated:
            if request.method == "POST":
                if form.is_valid():
                    add_record = form.save()
                    messages.success(request, "Record Successfully Added")
                    return redirect('home')
            return render(request, 'add_record.html', {"form": form})
        
        else:
            messages.success(request, "You have to login to add a record.")
            return redirect('home')

