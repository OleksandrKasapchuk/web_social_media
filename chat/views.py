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
    user_to_chat = get_object_or_404(CustomUser, pk=pk)
    chat = Chat.objects.filter(participants=request.user).filter(participants=user_to_chat).first()
    
    if chat:
        return redirect('chat:chat_detail', pk=chat.pk)
    else:
        new_chat = Chat.objects.create()
        new_chat.participants.add(request.user, user_to_chat)
        return redirect('chat:chat_detail', pk=new_chat.pk)


class DeleteMessageView(LoginRequiredMixin, View):
    def delete(self, request, pk, *args, **kwargs):
        message = get_object_or_404(Message, pk=pk)
        if request.user == message.user:
            message.delete()
            return JsonResponse({'success': True, 'message': 'Message deleted successfully.'})
        else:
            return JsonResponse({'success': False, 'message': 'You do not have permission to delete this message.'}, status=403)