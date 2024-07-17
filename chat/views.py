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


# @login_required
# def chat_list(request):
#     chats = request.user.chats.all()
#     # Додатковий контекст для учасників чату
#     chat_participants = []
#     for chat in chats:
#         participant = chat.participants.exclude(id=request.user.id).first()
#         chat_participants.append({
#             'chat': chat,
#             'participant': participant
#         })
#     return render(request, 'chat/chat_list.html', {'chat_participants': chat_participants})

# @login_required
# def chat_detail(request, pk):
#     chat = get_object_or_404(Chat, id=pk)
#     if request.user not in chat.participants.all():
#         return redirect('chat_list')

#     if request.method == "POST":
#         content = request.POST.get('content')
#         if content:
#             try:
#                 message = Message.objects.create(
#                     chat=chat,
#                     user=request.user,
#                     content=content
#                 )
#                 if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#                     return JsonResponse({
#                         'success': True,
#                         'username': request.user.username,
#                         'content': message.content,
#                         'avatar_url': request.user.avatar.url if request.user.avatar else "/static/images/default_avatar.jpg"
#                     })
#                 return redirect('chat_detail', chat_id=chat.pk)
#             except Exception as e:
#                 if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#                     return JsonResponse({'success': False, 'error': str(e)})
#                 raise e

#     participant = chat.participants.exclude(id=request.user.pk).first()
#     return render(request, 'chat/chat_detail.html', {'chat': chat, 'participant': participant})

class ChatListView(LoginRequiredMixin, ListView):
    model = Chat
    template_name = 'chat/chat_list.html'
    context_object_name = 'chats'

    def get_queryset(self):
        return self.request.user.chats.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        chat_participants = []
        for chat in context['chats']:
            participant = chat.participants.exclude(id=self.request.user.id).first()
            chat_participants.append({
                'chat': chat,
                'participant': participant
            })
        context['chat_participants'] = chat_participants
        return context


class ChatDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        chat = get_object_or_404(Chat, id=pk)
        if request.user not in chat.participants.all():
            return redirect('chat:chat_list')

        participant = chat.participants.exclude(id=request.user.pk).first()
        return render(request, 'chat/chat_detail.html', {'chat': chat, 'participant': participant})

    def post(self, request, pk):
        chat = get_object_or_404(Chat, id=pk)
        if request.user not in chat.participants.all():
            return JsonResponse({'success': False, 'error': 'Unauthorized'}, status=403)

        content = request.POST.get('content')
        if not content:
            return JsonResponse({'success': False, 'error': 'No content provided'}, status=400)

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
                    'avatar_url': request.user.avatar.url
                })
            return redirect('chat:chat_detail', pk=chat.pk)
        except Exception as e:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': str(e)})
            raise e


class ChatMessagesView(LoginRequiredMixin, View):
    def get(self, request, pk):
        chat = get_object_or_404(Chat, id=pk)
        if request.user not in chat.participants.all():
            return JsonResponse({'success': False, 'error': 'Unauthorized'}, status=403)

        messages = Message.objects.filter(chat=chat).order_by('timestamp')
        messages_data = []
        for message in messages:
            messages_data.append({
                'content': message.content,
                'avatar_url': message.user.avatar.url,
                'is_user_message': message.user == request.user,
                'delete_url': reverse_lazy('chat:delete_message', args=[message.chat.pk, message.pk])
            })

        return JsonResponse({'success': True, 'messages': messages_data})

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