# tasks/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Task
from .forms import TaskForm, CustomUserCreationForm

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful. You can now log in.")
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


@login_required
def home(request):
    tasks = Task.objects.filter(user=request.user)

    status = request.GET.get('status')
    priority = request.GET.get('priority')

    if status == 'completed':
        tasks = tasks.filter(is_completed=True)
    elif status == 'pending':
        tasks = tasks.filter(is_completed=False)

    if priority:
        tasks = tasks.filter(priority=priority)

    return render(request, 'home.html', {'tasks': tasks})


@login_required
def task_create(request):
    form = TaskForm(request.POST or None)
    if form.is_valid():
        task = form.save(commit=False)
        task.user = request.user
        task.save()
        messages.success(request, "Task created.")
        return redirect('home')
    return render(request, 'task_form.html', {'form': form})


@login_required
def task_update(request, pk):
    task = Task.objects.get(pk=pk, user=request.user)
    form = TaskForm(request.POST or None, instance=task)
    if form.is_valid():
        form.save()
        messages.success(request, "Task updated.")
        return redirect('home')
    return render(request, 'task_form.html', {'form': form})


@login_required
def task_delete(request, pk):
    task = Task.objects.get(pk=pk, user=request.user)
    task.delete()
    messages.success(request, "Task deleted.")
    return redirect('home')
