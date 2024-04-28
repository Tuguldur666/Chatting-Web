# views.py

from django.shortcuts import render, redirect, get_object_or_404,reverse
from django.contrib.auth.decorators import login_required
from .models import ChatRoom, Message
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q, Count

@login_required
def start_user_chat(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        other_user = User.objects.get(id=user_id) 
        rooms = ChatRoom.objects.annotate(num_members=Count('members')).filter(
            num_members=2,
            members=request.user
        ).filter(members=other_user)

        if rooms.exists():
            room = rooms.first() 
        else:
            room = ChatRoom.objects.create(is_group=False)
            room.members.set([request.user, other_user])  

        return HttpResponseRedirect(reverse('user_chat', args=[room.id]))

    chat_rooms = ChatRoom.objects.filter(members=request.user).distinct()
    chat_rooms_with_participants = []

    for room in chat_rooms:
        participants = room.members.exclude(id=request.user.id)
        participant_names = ', '.join([u.username for u in participants])
        if participant_names: 
            chat_rooms_with_participants.append({
                'room': room,
                'participants': participant_names
            })

    users = User.objects.exclude(id=request.user.id).exclude(chatrooms__in=chat_rooms)
    return render(request, 'start_user_chat.html', {
        'chat_rooms_with_participants': chat_rooms_with_participants,
        'users': users
    })


@login_required
def user_chat(request, room_id):
    room = get_object_or_404(ChatRoom, id=room_id)
    messages = room.messages.all().order_by('timestamp')
    if request.method == 'POST':
        message = Message.objects.create(
            chat_room=room,
            sender=request.user,
            message=request.POST.get('message')
        )
        return redirect('user_chat', room_id=room.id)
    return render(request, 'user_chat.html', {'room': room, 'messages': messages})
@login_required
def create_group_chat(request):
    if request.method == 'POST':
        room_name = request.POST.get('room_name')
        user_ids = request.POST.getlist('user_ids')
        if room_name and user_ids:
            room = ChatRoom.objects.create(name=room_name, is_group=True)
            room.members.add(request.user, *user_ids)  
            return redirect('group_chat', room_id=room.id)
        
    users = User.objects.exclude(id=request.user.id)  
    group_chats = ChatRoom.objects.filter(members=request.user, is_group=True)
    return render(request, 'create_group_chat.html', {'users': users, 'group_chats': group_chats})

@login_required
def group_chat(request, room_id):
    room = get_object_or_404(ChatRoom, id=room_id)
    if request.method == 'POST':
        message = request.POST.get('message')
        Message.objects.create(chat_room=room, sender=request.user, message=message)
    messages = room.messages.all().order_by('timestamp')
    return render(request, 'group_chat.html', {'room': room, 'messages': messages})

@login_required
def delete_chat_room(request, room_id):
    if request.method == 'POST':
        room = ChatRoom.objects.get(id=room_id)
        if room:
            room.delete()
        return redirect(reverse('start_user_chat'))
    return redirect(reverse('start_user_chat'))

@login_required
def delete_group_chat(request, room_id):
    if request.method == 'POST':
        room = get_object_or_404(ChatRoom, id=room_id)
        if room and room.is_group:
            room.delete()
        return redirect('create_group_chat')
    return redirect('create_group_chat')

