from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your Account Has Ben Created Successfully')
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {"form": form})