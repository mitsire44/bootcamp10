from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
# from .forms import NoteForm
# from .models import note
from django.contrib.auth.decorators import login_required
from .models import Profile
# Create your views here.

def home(request):
    context = {}
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        context['loyalty_points'] = profile.loyalty_points
    return render(request, 'rewards/home.html', context)

def signupuser(request):
    context = {'form':UserCreationForm()}
    if request.method=="GET":
        return render(request, 'rewards/signupuser.html', context)
    else:
        if request.POST['password1']==request.POST['password2']:
            try:
                user=User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('rewards')

            except IntegrityError:
                return render(request, 'rewards/signupuser.html', {'form':UserCreationForm(), 'error':'The username is taken!'})
        else:
            return render(request, 'rewards/signupuser.html', {'form':UserCreationForm(), 'error':'Passwords did not match!'})

def loginuser(request):
    if request.method=='GET':
        return render(request, 'rewards/loginuser.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username = request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'rewards/loginuser.html', {'form':AuthenticationForm(), 'error':'The username and password did not match'})
        else:
            login(request, user)
            return redirect('rewards')

@login_required
def logoutuser(request):
    logout(request)
    return redirect('home')

def rewards(request):
    profile = Profile.objects.get(user=request.user)
    context = {'loyalty_points': profile.loyalty_points}
    return render(request, 'rewards/rewards.html', context)

def simulator(request):
    profile = Profile.objects.get(user=request.user)
    context = {'loyalty_points': profile.loyalty_points}
    return render(request, 'rewards/simulator.html', context)

def addcard(request):
    pass
