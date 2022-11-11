from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import *

from main_app.forms import TaskForm, AddUserForm
from main_app.models import Task, Q


# Create your views here.


class TaskView(ListView):
    model = Task
    template_name = 'main.html'
    context_object_name = 'tasks'

    # def get_queryset(self):
    #     # return Task.objects.filter(author=self.request.user.id)
    #     return Task.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['count'] = self.get_queryset().count()

        search_input = self.request.GET.get('search')
        if search_input:
            context['tasks'] = Task.objects.filter(title__icontains=search_input)
            context['count'] = context['tasks'].count()

        return context


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'task_detail.html'
    context_object_name = 'task'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class TaskViewAuthor(ListView):
    model = Task
    template_name = 'main.html'
    context_object_name = 'tasks'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['count'] = self.get_queryset().count()
        return context

    def get_queryset(self):
        return Task.objects.filter(author__id=self.kwargs['pk'])


class AddTask(LoginRequiredMixin, CreateView):
    form_class = TaskForm
    template_name = 'add_task.html'
    success_url = reverse_lazy('main')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class EditTask(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'add_task.html'


class DeleteTask(LoginRequiredMixin, View):

    def get(self, request, pk):
        task = Task.objects.get(id=pk)
        if self.request.user == task.author:
            ctx = {
                'task': task,
            }
            return render(request, 'delete.html', ctx)

    def post(self, request, pk):
        task = Task.objects.get(id=pk)
        if self.request.user == task.author:
            task.delete()
            return redirect('main')


class CustomLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('main')


class CustomLogoutView(LoginRequiredMixin, LogoutView):
    def get_success_url(self):
        return reverse_lazy('main')


def registration_view(request):
    if request.method == 'POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('main')
    else:
        form = AddUserForm()
        context = {
            'form': form
        }
        return render(request, 'login.html', context)
