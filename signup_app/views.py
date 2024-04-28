from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect
from .forms import SignUpForm, UserDetailForm
from basic_app.models import UserProfile
from django.contrib.auth.decorators import login_required

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('login'))
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def user_details(request):
    user = request.user
    try:
        profile = user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile(user=user)
        profile.save()

    if request.method == 'POST':
        form = UserDetailForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('user_details'))
    else:
        form = UserDetailForm(instance=profile)

    return render(request, 'detail.html', {'form': form})
