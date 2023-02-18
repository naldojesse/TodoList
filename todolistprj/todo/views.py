from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView 
from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse_lazy
from . models import Task


# Create your views here.
# def home(request):
#     return HttpResponse("Working")

class TaskList(LoginRequiredMixin, ListView):
    model = Task 
    context_object_name = 'task'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # filters for each particular user
        context['task'] = context['task'].filter(user=self.request.user)
        
        # checks for incomplete tasks
        context['count'] = context['task'].filter(complete=False).count()
        return context
    
class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'todo/task.html'
    
# importing CreateView generic view for creating tasks
class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = "__all__"
    # fields = ['title', 'description' ]
    success_url = reverse_lazy('task')
    
class TaskUpdate(LoginRequiredMixin, UpdateView): 
    model = Task
    fields = "__all__"
    success_url = reverse_lazy("task")
    
class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy("task")
    
class CustomLoginView(LoginView):
    template_name = 'todo/login.html'
    fields = "__all__"
    redirect_authenticated_user = False 
    
    def get_success_url(self):
        return reverse_lazy("task")