from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.generic import View, ListView, DetailView, TemplateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from .models import Chat, Message
from auth_system.models import CustomUser
from post_system.mixins import *


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
def chat_detail(request, pk):
    chat = get_object_or_404(Chat, id=pk)
    if request.user not in chat.participants.all():
        return redirect('chat_list')

    if request.method == "POST":
        content = request.POST.get('content')
        if content:
            try:
                message = Message.objects.create(
                    chat=chat,
                    user=request.user,
                    content=content
                )
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': True,
                        'username': request.user.username,
                        'content': message.content,
                        'avatar_url': request.user.avatar.url if request.user.avatar else "/static/images/default_avatar.jpg"
                    })
                return redirect('chat_detail', chat_id=chat.pk)
            except Exception as e:
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'success': False, 'error': str(e)})
                raise e

    participant = chat.participants.exclude(id=request.user.pk).first()
    return render(request, 'chat/chat_detail.html', {'chat': chat, 'participant': participant})


# class ChatDetailView(View):
#     def get(self, request, chat_id):
#         chat = get_object_or_404(Chat, id=chat_id)
#         if request.user not in chat.participants.all():
#             return redirect('chat_list')
#         participant = chat.participants.exclude(id=request.user.id).first()
#         return render(request, 'chat/chat_detail.html', {'chat': chat, 'participant': participant})

#     def post(self, request, chat_id):
#         chat = get_object_or_404(Chat, id=chat_id)
#         if request.user not in chat.participants.all():
#             return JsonResponse({'success': False, 'error': 'Unauthorized'}, status=403)

#         content = request.POST.get('content')
#         if not content:
#             return JsonResponse({'success': False, 'error': 'No content provided'}, status=400)

#         message = Message.objects.create(
#             chat=chat,
#             sender=request.user,
#             content=content
#         )

#         return JsonResponse({
#             'success': True,
#             'content': message.content,
#             'username': message.sender.username,
#             'avatar_url': message.sender.avatar.url,
#             'is_user_message': message.sender == request.user,
#             'delete_url': reverse_lazy('chat:delete_message', args=[message.chat.pk, message.pk])
#         })


# class ChatMessagesView(View):
#     def get(self, request, chat_id):
#         chat = get_object_or_404(Chat, id=chat_id)
#         if request.user not in chat.participants.all():
#             return JsonResponse({'success': False, 'error': 'Unauthorized'}, status=403)

#         messages = Message.objects.filter(chat=chat).order_by('timestamp')
#         messages_data = []
#         for message in messages:
#             messages_data.append({
#                 'content': message.content,
#                 'username': message.sender.username,
#                 'avatar_url': message.sender.avatar.url,
#                 'is_user_message': message.sender == request.user,
#                 'delete_url': reverse_lazy('chat:delete_message', args=[message.chat.pk, message.pk])
#             })

#         return JsonResponse({'success': True, 'messages': messages_data})

@login_required
def start_chat(request, pk):
    user_to = get_object_or_404(CustomUser, id=pk)
    chat = Chat.objects.filter(participants=request.user).filter(participants=user_to).first()
    
    if not chat:
        chat = Chat.objects.create()
        chat.participants.add(request.user, user_to)
    
    return redirect('chat_detail', chat_id=chat.pk)


class DeleteMessageView(LoginRequiredMixin, UserIsOwnerMixin,DeleteView):
    model = Message
    template_name = 'form.html'
    
    def get_success_url(self):
        return reverse_lazy('chat:chat_detail', kwargs={"pk": self.kwargs['chat_id']})