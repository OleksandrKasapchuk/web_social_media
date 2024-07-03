# from django.shortcuts import render, redirect
# from chat.models import Room, Message
# from django.http import HttpResponse, JsonResponse

# # Create your views here.
# def home(request):
#     return render(request, 'chat/home.html')

# def room(request, room):
#     username = request.GET.get('username')
#     room_details = Room.objects.get(name=room)
#     return render(request, 'chat/room.html', {
#         'username': username,
#         'room': room,
#         'room_details': room_details
#     })

# def checkview(request):
#     room = request.POST['room_name']
#     username = request.POST['username']

#     if not Room.objects.filter(name=room).exists():
#         new_room = Room.objects.create(name=room)
#         new_room.save()
#     return redirect('/chat/ '+room+'/?username='+username)

# def send(request):
#     message = request.POST['message']
#     username = request.POST['username']
#     room_id = request.POST['room_id']

#     new_message = Message.objects.create(value=message, user=username, room=room_id)
#     new_message.save()
#     return HttpResponse('Message sent successfully')

# def getMessages(request, room):
#     room_details = Room.objects.get(name=room)

#     messages = Message.objects.filter(room=room_details.id)
#     return JsonResponse({"messages":list(messages.values())})


# chat/views.py
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Chat, Message
from .forms import MessageForm

@login_required
def chat_list(request):
    chats = request.user.chats.all()
    # Додатковий контекст для учасників чату
    chat_participants = []
    for chat in chats:
        participant = chat.participants.exclude(id=request.user.id).first()
        chat_participants.append({
            'chat': chat,
            'participant': participant
        })
    return render(request, 'chat/chat_list.html', {'chat_participants': chat_participants})

@login_required
def chat_detail(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    if request.user not in chat.participants.all():
        return redirect('chat_list')

    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.chat = chat
            message.sender = request.user
            message.save()
            return redirect('chat_detail', chat_id=chat.id)
    else:
        form = MessageForm()

    participant = chat.participants.exclude(id=request.user.id).first()
    return render(request, 'chat/chat_detail.html', {'chat': chat, 'form': form, 'participant': participant})

@login_required
def start_chat(request, user_id):
    user_to = get_object_or_404(get_user_model(), id=user_id)
    chat = Chat.objects.filter(participants=request.user).filter(participants=user_to).first()
    
    if not chat:
        chat = Chat.objects.create()
        chat.participants.add(request.user, user_to)
    
    return redirect('chat_detail', chat_id=chat.id)