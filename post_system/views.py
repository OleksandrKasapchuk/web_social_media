from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from .models import *
from django.views.generic import View, ListView, DetailView, CreateView, TemplateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin




class Index(TemplateView):
	template_name = "post_system/index.html"


# class DashboardListView(LoginRequiredMixin, ListView):
# 	model = Dashboard
# 	context_object_name = "dashboards"
# 	template_name = "task_tracker/dashboards.html"


# class DashboardCreateView(LoginRequiredMixin, CreateView):
# 	model = Dashboard
# 	template_name = "task_tracker/form.html"
# 	form_class = DashboardCreateForm
	
# 	def form_valid(self, form):
# 		form.instance.creator = self.request.user
# 		return super().form_valid(form)
	
# 	def get_success_url(self) -> str:
# 		return reverse_lazy("task-tracker:dashboard-list")


# class DashboardUpdateView(LoginRequiredMixin, UserIsOwnerMixin, UpdateView):
# 	model = Dashboard
# 	template_name = "task_tracker/form.html"
# 	form_class = DashboardCreateForm
	

# 	def get_success_url(self) -> str:
# 		return reverse_lazy("task-tracker:dashboard-list")

# class DashboardDeleteView(LoginRequiredMixin, UserIsOwnerMixin, DeleteView):
# 	model = Dashboard
# 	template_name = "task_tracker/form.html"
	
# 	def get_success_url(self) -> str:
# 		return reverse_lazy("task-tracker:dashboard-list")


# class TaskListView(LoginRequiredMixin, ListView):
# 	model = Task
# 	context_object_name = "tasks"
# 	template_name = "task_tracker/tasks.html"

# 	def get_context_data(self, **kwargs):
# 		context = super().get_context_data(**kwargs)
# 		context['dashboard_pk'] = self.kwargs['dashboard_pk']
# 		context['form'] = FilterTaskForm(self.request.GET)
# 		return context
	
# 	def get_queryset(self):
# 		queryset = super().get_queryset()
# 		priority = self.request.GET.get("priority", "")
# 		end_date = self.request.GET.get("end_date","")
# 		if priority:
# 			if priority == "4":
# 				queryset = queryset.all()
# 			else:
# 				queryset = queryset.filter(priority=priority)
# 		if end_date:
# 			queryset = queryset.filter(active=True)
# 		return queryset.filter(dashboard_id=self.kwargs['dashboard_pk'])


# class TaskDetailView(DetailView):
# 	model = Task
# 	context_object_name = "task"
# 	template_name = "task_tracker/task_details.html"

# 	def get_context_data(self, **kwargs):
# 		context = super().get_context_data(**kwargs)
# 		context['dashboard_pk'] = self.kwargs['dashboard_pk']
# 		task = self.get_object()
# 		context['comments'] = Comment.objects.filter(task=task)
# 		context['form'] = CommentForm
# 		return context
	
# 	def post(self, request, *args, **kwargs):
# 		comment_form = CommentForm(request.POST, request.FILES)
# 		if comment_form.is_valid():
# 			comment = comment_form.save(commit=False)
# 			comment.creator = request.user
# 			comment.task = self.get_object()
# 			comment.save()
# 			return redirect("task-tracker:task-details", dashboard_pk=comment.task.dashboard.pk, pk=comment.task.pk)
# 		else:
# 			pass

# class TaskCreateView(LoginRequiredMixin, CreateView):
# 	model = Task
# 	template_name = "task_tracker/form.html"
# 	form_class = TaskCreateForm
# 	def form_valid(self, form):
# 		form.instance.creator = self.request.user
# 		form.instance.dashboard = Dashboard.objects.get(id=self.kwargs['dashboard_pk'])
# 		form.instance.end_date = form.cleaned_data['end_date']
# 		return super().form_valid(form)
# 	def get_success_url(self) -> str:
# 		return reverse_lazy("task-tracker:task-list",  kwargs={'dashboard_pk': self.kwargs['dashboard_pk']})


# class TaskUpdateView(LoginRequiredMixin, UserIsOwnerMixin, UpdateView):
# 	model = Task
# 	template_name = "task_tracker/form.html"
# 	context_object_name = "task"
# 	form_class = TaskCreateForm

# 	def get_success_url(self) -> str:
# 		return reverse_lazy("task-tracker:task-details",  kwargs={'dashboard_pk': self.kwargs['dashboard_pk'],"pk": self.kwargs['pk']})


# class TaskDeleteView(LoginRequiredMixin, UserIsOwnerMixin, DeleteView):
# 	model = Task
# 	template_name = "task_tracker/form.html"

# 	def get_success_url(self) -> str:
# 		return reverse_lazy("task-tracker:task-list",  kwargs={'dashboard_pk': self.kwargs['dashboard_pk']})

# class CommentLikeToggle(LoginRequiredMixin, View):
# 	def post(self, request, *args, **kwargs) :
# 		comment = get_object_or_404(Comment, pk=self.kwargs.get('pk'))
# 		like_qs = Like.objects.filter(comment=comment, user=request.user)
# 		if like_qs.exists():
# 			like_qs.delete()
# 		else:
# 			Like.objects.create(comment=comment, user=request.user)
# 		return redirect("task-tracker:task-details", dashboard_pk=self.kwargs['dashboard_pk'],pk=self.kwargs['task_pk'])
	
# class DeleteCommentView(LoginRequiredMixin,UserIsOwnerMixin,DeleteView):
# 	model = Comment
# 	template_name = "task_tracker/form.html"
# 	def get_success_url(self) -> str:
# 		return reverse_lazy("task-tracker:task-details",  kwargs={'dashboard_pk': self.kwargs['dashboard_pk'],"pk": self.kwargs['task_pk']})

# class UpdateCommentView(LoginRequiredMixin,UserIsOwnerMixin,UpdateView):
# 	model = Comment
# 	template_name = "task_tracker/form.html"
# 	context_object_name = "comment"
# 	form_class = CommentForm
# 	def get_success_url(self) -> str:
# 		return reverse_lazy("task-tracker:task-details",  kwargs={'dashboard_pk': self.kwargs['dashboard_pk'],"pk": self.kwargs['task_pk']})