from django.shortcuts import render,reverse 
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from chat_app.models import *

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login')) 


def index(request):
    if request.user.is_authenticated:
        default_room = ChatRoom.objects.filter(members=request.user).first()
        default_group_room = ChatRoom.objects.filter(members=request.user, is_group=True).first()
        context = {
            'default_room_id': default_room.id if default_room else None,
            'default_group_room_id': default_group_room.id if default_group_room else None
        }
    else:
        context = {
            'default_room_id': None,
            'default_group_room_id': None
        }
    return render(request, 'index.html', context)
